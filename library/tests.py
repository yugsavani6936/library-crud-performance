from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Book, BenchmarkResult
from .benchmark import execute_benchmark_suite


class LibraryCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='testpassword123')
        self.book = Book.objects.create(
            title='Higher Engineering Mathematics',
            author='Dr. B. S. Grewal',
            isbn='978-8174091955',
            category='Mathematics',
            publication_year=2021,
            available_copies=5,
            is_benchmark=False
        )

    def test_book_str(self):
        self.assertIn('Higher Engineering Mathematics', str(self.book))

    def test_book_list_view(self):
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Higher Engineering Mathematics')

    def test_book_search(self):
        response = self.client.get(reverse('book_list') + '?q=Grewal')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dr. B. S. Grewal')

    def test_book_create_authenticated(self):
        self.client.login(username='tester', password='testpassword123')
        response = self.client.post(reverse('book_create'), {
            'title': 'Basic Electrical Engineering',
            'author': 'Prof. V. K. Mehta',
            'isbn': '978-8121908719',
            'category': 'Electronics',
            'publication_year': 2022,
            'available_copies': 8
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Book.objects.filter(isbn='978-8121908719').exists())

    def test_book_update(self):
        self.client.login(username='tester', password='testpassword123')
        response = self.client.post(reverse('book_update', args=[self.book.pk]), {
            'title': 'Higher Engineering Mathematics (Updated Edition)',
            'author': 'Dr. B. S. Grewal',
            'isbn': '978-8174091955',
            'category': 'Mathematics',
            'publication_year': 2023,
            'available_copies': 12
        })
        self.assertEqual(response.status_code, 302)
        self.book.refresh_from_db()
        self.assertEqual(self.book.publication_year, 2023)
        self.assertEqual(self.book.available_copies, 12)

    def test_book_delete(self):
        self.client.login(username='tester', password='testpassword123')
        response = self.client.post(reverse('book_delete', args=[self.book.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Book.objects.filter(pk=self.book.pk).exists())


class BenchmarkEngineTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='benchmarker', password='testpassword123')

    def test_benchmark_suite_execution(self):
        # Execute benchmark for 100 records, 1 trial for all operations
        results = execute_benchmark_suite(
            operations=['CREATE', 'READ', 'UPDATE', 'DELETE'],
            dataset_size=100,
            trials=1
        )
        self.assertEqual(len(results), 4)
        for r in results:
            self.assertGreater(r.execution_time_ns, 0)
            self.assertGreater(r.execution_time_ms, 0)
            self.assertEqual(r.dataset_size, 100)

        # Ensure no benchmark records leak into permanent catalog
        self.assertEqual(Book.objects.filter(is_benchmark=True).count(), 0)

    def test_csv_export(self):
        # Seed a dummy benchmark result
        BenchmarkResult.objects.create(
            operation='CREATE',
            dataset_size=100,
            trial_number=1,
            execution_time_ns=15000000,
            database_name='PostgreSQL 18',
            notes='Test measurement'
        )
        self.client.login(username='benchmarker', password='testpassword123')
        response = self.client.get(reverse('export_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn(b'Trial ID,Operation,Dataset Size', response.content)
