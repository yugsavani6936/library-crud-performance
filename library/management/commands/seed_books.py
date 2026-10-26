from django.core.management.base import BaseCommand
from library.models import Book

class Command(BaseCommand):
    help = "Seeds initial library records with Indian engineering textbooks and Hindu authors"

    def handle(self, *args, **options):
        sample_books = [
            ("Higher Engineering Mathematics", "Dr. B. S. Grewal", "978-8174091955", "Mathematics", 2021, 8),
            ("A Textbook of Engineering Mathematics", "Dr. N. P. Bali and Dr. Manish Goyal", "978-8131808320", "Mathematics", 2020, 6),
            ("Database Management Systems: Concepts & Design", "Prof. R. P. Mahapatra & Dr. P. K. Sharma", "978-8120349889", "Computer Science", 2022, 10),
            ("Design and Analysis of Algorithms", "Dr. S. R. Jayswal and Dr. Anuradha Mishra", "978-9389588231", "Computer Science", 2021, 5),
            ("Computer Networks and Internet Technology", "Dr. Rajesh K. Shukla", "978-8120345678", "Information Technology", 2019, 7),
            ("Object Oriented Programming with C++", "Prof. E. Balagurusamy", "978-9352607990", "Computer Science", 2020, 12),
            ("A Textbook of Fluid Mechanics and Hydraulic Machines", "Dr. R. K. Bansal", "978-8131808153", "Mechanical", 2018, 5),
            ("Engineering Thermodynamics", "Prof. P. K. Nag", "978-9352606429", "Mechanical", 2019, 6),
            ("A Course in Electrical and Electronic Measurements", "Prof. A. K. Sawhney and Puneet Sawhney", "978-8177001013", "Electronics", 2017, 7),
            ("Basic Electrical Engineering", "Prof. V. K. Mehta and Rohit Mehta", "978-8121908719", "Electronics", 2022, 9),
            ("Control Systems Engineering", "Dr. I. J. Nagrath and Dr. M. Gopal", "978-9389811414", "Electronics", 2021, 4),
            ("Digital Circuits and Logic Design", "Dr. Sanjay Sharma", "978-9350143896", "Electronics", 2020, 8),
            ("Surveying and Levelling (Vol. 1)", "Dr. B. C. Punmia, Ashok Kumar Jain, Arun Kumar Jain", "978-8170088530", "Civil", 2016, 6),
            ("Building Construction", "Dr. Sushil Kumar", "978-8180140228", "Civil", 2018, 5),
            ("Software Engineering: Principles and Practices", "Dr. Rohit Khurana", "978-9325994270", "Information Technology", 2021, 6),
            ("Operating Systems: Principles and Design", "Prof. Dhananjay M. Dhamdhere", "978-0070611948", "Computer Science", 2019, 5),
        ]

        created_count = 0
        for title, author, isbn, category, pub_year, copies in sample_books:
            obj, created = Book.objects.get_or_create(
                isbn=isbn,
                defaults={
                    "title": title,
                    "author": author,
                    "category": category,
                    "publication_year": pub_year,
                    "available_copies": copies,
                    "is_benchmark": False
                }
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {created_count} library books with Indian author records."))
