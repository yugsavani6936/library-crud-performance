import csv
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Min, Max, Count
from django.http import HttpResponse, JsonResponse
from .models import Book, BenchmarkResult
from .forms import BookForm
from .benchmark import execute_benchmark_suite, cleanup_benchmark_records


# ==========================================
# Feature 1: Library Management Views
# ==========================================

def book_list(request):
    """
    Displays the catalog of books with search, filter, and pagination.
    Only genuine library records (is_benchmark=False) are presented.
    """
    search_query = request.GET.get('q', '').strip()
    category_filter = request.GET.get('category', '').strip()

    books = Book.objects.filter(is_benchmark=False)

    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(isbn__icontains=search_query)
        )

    if category_filter:
        books = books.filter(category=category_filter)

    # Statistics for dashboard summary cards
    total_books = Book.objects.filter(is_benchmark=False).count()
    categories = Book.CATEGORY_CHOICES

    # Pagination: 10 books per page
    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'category_filter': category_filter,
        'total_books': total_books,
        'categories': categories,
    }
    return render(request, 'library/book_list.html', context)


@login_required
def book_create(request):
    """
    Adds a new book record to the library inventory.
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.is_benchmark = False
            book.save()
            messages.success(request, f'Book "{book.title}" added successfully!')
            return redirect('book_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookForm()

    return render(request, 'library/book_form.html', {
        'form': form,
        'title': 'Add New Book',
        'button_text': 'Add Book to Catalog'
    })


@login_required
def book_update(request, pk):
    """
    Edits an existing book record.
    """
    book = get_object_or_404(Book, pk=pk, is_benchmark=False)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, f'Book "{book.title}" updated successfully!')
            return redirect('book_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookForm(instance=book)

    return render(request, 'library/book_form.html', {
        'form': form,
        'book': book,
        'title': f'Edit Book: {book.title}',
        'button_text': 'Save Changes'
    })


@login_required
def book_delete(request, pk):
    """
    Deletes a book after user confirmation.
    """
    book = get_object_or_404(Book, pk=pk, is_benchmark=False)
    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f'Book "{title}" was deleted from the catalog.')
        return redirect('book_list')

    return render(request, 'library/book_confirm_delete.html', {'book': book})


# ==========================================
# Feature 2: Performance Benchmarking Views
# ==========================================

@login_required
def benchmark_view(request):
    """
    Executes empirical performance tests for CREATE, READ, UPDATE, and DELETE.
    Captures database execution durations using high-resolution timers.
    """
    results = None
    selected_ops = []
    dataset_size = 100
    trials = 3

    if request.method == 'POST':
        selected_ops = request.POST.getlist('operations')
        try:
            dataset_size = int(request.POST.get('dataset_size', 100))
            trials = int(request.POST.get('trials', 3))
        except ValueError:
            dataset_size = 100
            trials = 3

        # Safety clamps for web responsiveness
        if dataset_size not in [50, 100, 500, 1000, 5000, 10000]:
            dataset_size = 100
        if trials < 1 or trials > 5:
            trials = 3

        if not selected_ops:
            messages.warning(request, 'Please select at least one CRUD operation to benchmark.')
        else:
            try:
                results = execute_benchmark_suite(
                    operations=selected_ops,
                    dataset_size=dataset_size,
                    trials=trials
                )
                messages.success(
                    request,
                    f'Experiment successfully completed! {len(results)} trials recorded in PostgreSQL.'
                )
            except Exception as e:
                messages.error(request, f'Benchmark execution error: {str(e)}')

    # Recent 10 results for reference
    recent_results = BenchmarkResult.objects.order_by('-created_at')[:10]

    context = {
        'results': results,
        'selected_ops': selected_ops,
        'dataset_size': dataset_size,
        'trials': trials,
        'recent_results': recent_results,
    }
    return render(request, 'library/benchmark.html', context)


# ==========================================
# Feature 3: Results Dashboard & CSV Export
# ==========================================

def results_dashboard(request):
    """
    Displays aggregated analytics, comparison matrix, and visual charts
    based entirely on genuine recorded measurements in PostgreSQL.
    """
    # Summary Cards
    total_trials = BenchmarkResult.objects.count()
    distinct_sizes = BenchmarkResult.objects.values_list('dataset_size', flat=True).distinct().order_by('dataset_size')
    
    # Calculate averages grouped by (operation, dataset_size)
    aggregates = (
        BenchmarkResult.objects
        .values('operation', 'dataset_size')
        .annotate(
            avg_time_ns=Avg('execution_time_ns'),
            trial_count=Count('id'),
            min_time_ns=Min('execution_time_ns'),
            max_time_ns=Max('execution_time_ns')
        )
        .order_by('dataset_size', 'operation')
    )

    # Format matrix for table presentation: dict mapping op -> {size: avg_ms}
    operations = ['CREATE', 'READ', 'UPDATE', 'DELETE']
    table_matrix = {op: {} for op in operations}
    
    for row in aggregates:
        op = row['operation']
        size = row['dataset_size']
        avg_ms = round(row['avg_time_ns'] / 1_000_000.0, 3)
        if op in table_matrix:
            table_matrix[op][size] = avg_ms

    chart_sizes = list(distinct_sizes)

    # Format rows for crystal-clear template rendering
    table_rows = []
    for op in operations:
        cells = []
        for size in chart_sizes:
            avg_ms = table_matrix[op].get(size)
            cells.append({
                'size': size,
                'avg_ms': avg_ms
            })
        table_rows.append({
            'operation': op,
            'cells': cells
        })

    # Prepare JSON structures for Chart.js
    chart_datasets = []
    
    palette = {
        'CREATE': {'border': '#2d6a4f', 'bg': 'rgba(45, 106, 79, 0.7)'},
        'READ': {'border': '#1d3557', 'bg': 'rgba(29, 53, 87, 0.7)'},
        'UPDATE': {'border': '#d97706', 'bg': 'rgba(217, 119, 6, 0.7)'},
        'DELETE': {'border': '#b91c1c', 'bg': 'rgba(185, 28, 28, 0.7)'},
    }

    for op in operations:
        data_points = [table_matrix[op].get(size, 0) for size in chart_sizes]
        chart_datasets.append({
            'label': op,
            'data': data_points,
            'borderColor': palette[op]['border'],
            'backgroundColor': palette[op]['bg'],
            'borderWidth': 2,
            'fill': False,
            'tension': 0.1
        })

    # Latest 25 individual trial records
    trial_records = BenchmarkResult.objects.all()[:25]

    context = {
        'total_trials': total_trials,
        'chart_sizes': chart_sizes,
        'chart_sizes_json': json.dumps([str(s) for s in chart_sizes]),
        'chart_datasets_json': json.dumps(chart_datasets),
        'operations': operations,
        'table_rows': table_rows,
        'trial_records': trial_records,
    }
    return render(request, 'library/results.html', context)


@login_required
def export_csv(request):
    """
    Exports all genuine experimental benchmark records to a downloadable CSV.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="library_crud_benchmark_results.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Trial ID',
        'Operation',
        'Dataset Size',
        'Trial Number',
        'Execution Time (ns)',
        'Execution Time (ms)',
        'Execution Time (s)',
        'Throughput (ops/sec)',
        'Database Engine',
        'Timestamp',
        'Notes'
    ])

    results = BenchmarkResult.objects.all().order_by('dataset_size', 'operation', 'trial_number')
    for r in results:
        writer.writerow([
            r.id,
            r.operation,
            r.dataset_size,
            r.trial_number,
            r.execution_time_ns,
            r.execution_time_ms,
            r.execution_time_s,
            r.throughput_ops_per_sec,
            r.database_name,
            r.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            r.notes
        ])

    return response


@login_required
def clear_benchmarks(request):
    """
    Clears all saved benchmark measurements upon user confirmation.
    """
    if request.method == 'POST':
        count, _ = BenchmarkResult.objects.all().delete()
        messages.success(request, f'Cleared {count} benchmark results from PostgreSQL.')
    return redirect('results_dashboard')

