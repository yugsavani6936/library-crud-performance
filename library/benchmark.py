"""
Benchmarking Engine for Experimental Performance Evaluation of CRUD Operations
Uses high-resolution Python time.perf_counter_ns() to accurately measure
PostgreSQL relational database operation durations across varying dataset sizes.
"""

import time
import random
from django.db import transaction
from .models import Book, BenchmarkResult

# Realistic Indian Hindu names for generated benchmark records
INDIAN_FIRST_NAMES = [
    "Aarav", "Aditya", "Vikram", "Rajesh", "Rohit", "Siddharth",
    "Suresh", "Amit", "Deepak", "Manoj", "Alok", "Gaurav",
    "Pradeep", "Ashok", "Ramesh", "Dinesh", "Kunal", "Naveen"
]

INDIAN_LAST_NAMES = [
    "Sharma", "Verma", "Gupta", "Patel", "Mishra", "Joshi",
    "Rao", "Reddy", "Chauhan", "Bhat", "Iyer", "Nair",
    "Pandey", "Saxena", "Agarwal", "Dubey", "Trivedi", "Shukla"
]

CATEGORIES = [
    'Computer Science', 'Information Technology', 'Electronics',
    'Mechanical', 'Civil', 'Mathematics', 'Physics'
]


def generate_benchmark_records(count, prefix=""):
    """
    Constructs in-memory Book instances with Indian author names.
    This preparation step is executed outside the timing window.
    """
    records = []
    base_timestamp = int(time.time() * 1000) % 10000000
    for i in range(count):
        fname = INDIAN_FIRST_NAMES[i % len(INDIAN_FIRST_NAMES)]
        lname = INDIAN_LAST_NAMES[(i // len(INDIAN_FIRST_NAMES)) % len(INDIAN_LAST_NAMES)]
        author = f"Dr. {fname} {lname}"
        title = f"Engineering Principles and Research Vol. {i+1}"
        isbn = f"978-{prefix}-{base_timestamp}-{i:05d}"
        category = CATEGORIES[i % len(CATEGORIES)]
        pub_year = 2000 + (i % 25)
        
        records.append(Book(
            title=title,
            author=author,
            isbn=isbn,
            category=category,
            publication_year=pub_year,
            available_copies=5,
            is_benchmark=True
        ))
    return records


def cleanup_benchmark_records():
    """
    Deletes all temporary benchmark records from the database.
    Normal library inventory records (is_benchmark=False) are preserved.
    """
    Book.objects.filter(is_benchmark=True).delete()


def ensure_benchmark_data(dataset_size, prefix="SETUP"):
    """
    Ensures that exactly `dataset_size` benchmark records are present in PostgreSQL
    for READ, UPDATE, or DELETE evaluations.
    """
    current_count = Book.objects.filter(is_benchmark=True).count()
    if current_count < dataset_size:
        cleanup_benchmark_records()
        records = generate_benchmark_records(dataset_size, prefix=prefix)
        Book.objects.bulk_create(records, batch_size=1000)
    elif current_count > dataset_size:
        cleanup_benchmark_records()
        records = generate_benchmark_records(dataset_size, prefix=prefix)
        Book.objects.bulk_create(records, batch_size=1000)


def benchmark_create(dataset_size, trial_number):
    """
    Evaluates CREATE operation:
    Measures time taken by PostgreSQL to execute batch INSERT for `dataset_size` records.
    """
    # 1. Prepare records in Python memory (un-timed)
    cleanup_benchmark_records()
    records = generate_benchmark_records(dataset_size, prefix=f"C{trial_number}")

    # 2. High-resolution database execution measurement
    start_ns = time.perf_counter_ns()
    Book.objects.bulk_create(records, batch_size=1000)
    duration_ns = time.perf_counter_ns() - start_ns

    # 3. Store result in PostgreSQL
    result = BenchmarkResult.objects.create(
        operation='CREATE',
        dataset_size=dataset_size,
        trial_number=trial_number,
        execution_time_ns=duration_ns,
        database_name='PostgreSQL 18',
        notes=f"Bulk insert of {dataset_size} records in batch size 1000"
    )

    # 4. Clean up benchmark records so subsequent runs start clean
    cleanup_benchmark_records()
    return result


def benchmark_read(dataset_size, trial_number):
    """
    Evaluates READ operation:
    Measures time taken by PostgreSQL to query and return `dataset_size` records,
    including Django ORM object materialization.
    """
    # 1. Ensure test data exists in PostgreSQL (un-timed)
    ensure_benchmark_data(dataset_size, prefix=f"R{trial_number}")

    # 2. High-resolution database execution measurement
    start_ns = time.perf_counter_ns()
    # list() forces immediate query execution and object fetching from PostgreSQL
    records = list(Book.objects.filter(is_benchmark=True)[:dataset_size])
    duration_ns = time.perf_counter_ns() - start_ns

    # 3. Store result in PostgreSQL
    result = BenchmarkResult.objects.create(
        operation='READ',
        dataset_size=dataset_size,
        trial_number=trial_number,
        execution_time_ns=duration_ns,
        database_name='PostgreSQL 18',
        notes=f"Full query fetch & materialization of {len(records)} records"
    )
    return result


def benchmark_update(dataset_size, trial_number):
    """
    Evaluates UPDATE operation:
    Measures time taken by PostgreSQL to execute bulk UPDATE query on `dataset_size` records.
    """
    # 1. Ensure test data exists in PostgreSQL (un-timed)
    ensure_benchmark_data(dataset_size, prefix=f"U{trial_number}")

    new_copies = 10 + (trial_number % 5)

    # 2. High-resolution database execution measurement
    start_ns = time.perf_counter_ns()
    updated_count = Book.objects.filter(is_benchmark=True).update(available_copies=new_copies)
    duration_ns = time.perf_counter_ns() - start_ns

    # 3. Store result in PostgreSQL
    result = BenchmarkResult.objects.create(
        operation='UPDATE',
        dataset_size=dataset_size,
        trial_number=trial_number,
        execution_time_ns=duration_ns,
        database_name='PostgreSQL 18',
        notes=f"Bulk UPDATE query modifying copies to {new_copies} for {updated_count} rows"
    )
    return result


def benchmark_delete(dataset_size, trial_number):
    """
    Evaluates DELETE operation:
    Measures time taken by PostgreSQL to execute batch DELETE query on `dataset_size` records.
    """
    # 1. Ensure test data exists in PostgreSQL (un-timed)
    ensure_benchmark_data(dataset_size, prefix=f"D{trial_number}")

    # 2. High-resolution database execution measurement
    start_ns = time.perf_counter_ns()
    deleted_count, _ = Book.objects.filter(is_benchmark=True).delete()
    duration_ns = time.perf_counter_ns() - start_ns

    # 3. Store result in PostgreSQL
    result = BenchmarkResult.objects.create(
        operation='DELETE',
        dataset_size=dataset_size,
        trial_number=trial_number,
        execution_time_ns=duration_ns,
        database_name='PostgreSQL 18',
        notes=f"Batch DELETE removing {deleted_count} benchmark records"
    )
    return result


def execute_benchmark_suite(operations, dataset_size, trials=3):
    """
    Runs experimental trials for specified operations and dataset size.
    Returns list of newly recorded BenchmarkResult objects.
    """
    results = []
    
    # Map operation string to benchmark function
    dispatch = {
        'CREATE': benchmark_create,
        'READ': benchmark_read,
        'UPDATE': benchmark_update,
        'DELETE': benchmark_delete,
    }

    try:
        for trial in range(1, trials + 1):
            for op in operations:
                op_upper = op.upper()
                if op_upper in dispatch:
                    func = dispatch[op_upper]
                    res = func(dataset_size, trial)
                    results.append(res)
    finally:
        # Guarantee no leftover benchmark records pollute normal catalog
        cleanup_benchmark_records()

    return results
