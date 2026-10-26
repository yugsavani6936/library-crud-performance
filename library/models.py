from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

class Book(models.Model):
    """
    Represents a book in the library catalog.
    Used for day-to-day library management and for evaluating CRUD performance.
    """
    CATEGORY_CHOICES = [
        ('Computer Science', 'Computer Science'),
        ('Information Technology', 'Information Technology'),
        ('Electronics', 'Electronics'),
        ('Mechanical', 'Mechanical'),
        ('Civil', 'Civil'),
        ('Mathematics', 'Mathematics'),
        ('Physics', 'Physics'),
        ('General Literature', 'General Literature'),
        ('Other', 'Other'),
    ]

    title = models.CharField(max_length=255, help_text="Title of the book")
    author = models.CharField(max_length=255, help_text="Author of the book")
    isbn = models.CharField(
        max_length=20,
        unique=True,
        help_text="International Standard Book Number (must be unique)"
    )
    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES,
        default='Computer Science',
        help_text="Subject or genre category"
    )
    publication_year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1500),
            MaxValueValidator(datetime.date.today().year + 1)
        ],
        help_text="Year the book was published"
    )
    available_copies = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(0)],
        help_text="Number of copies currently available for issue"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when record was created"
    )
    
    # Flag to isolate performance evaluation records from genuine library inventory
    is_benchmark = models.BooleanField(
        default=False,
        db_index=True,
        help_text="True if created as temporary test record for benchmarking"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"


class BenchmarkResult(models.Model):
    """
    Stores genuine empirical performance metrics measured during CRUD evaluations.
    Stored in PostgreSQL for retrospective analysis and visualization.
    """
    OPERATION_CHOICES = [
        ('CREATE', 'CREATE (Batch Insert)'),
        ('READ', 'READ (Full Fetch & Materialize)'),
        ('UPDATE', 'UPDATE (Bulk Update)'),
        ('DELETE', 'DELETE (Batch Delete)'),
    ]

    operation = models.CharField(
        max_length=10,
        choices=OPERATION_CHOICES,
        help_text="CRUD operation evaluated"
    )
    dataset_size = models.PositiveIntegerField(
        help_text="Number of records operated on in this trial (e.g. 100, 1000, 10000)"
    )
    trial_number = models.PositiveIntegerField(
        default=1,
        help_text="Trial run number (1, 2, 3...)"
    )
    execution_time_ns = models.BigIntegerField(
        help_text="Measured database duration in nanoseconds using time.perf_counter_ns()"
    )
    database_name = models.CharField(
        max_length=100,
        default='PostgreSQL 18',
        help_text="Underlying relational database engine"
    )
    notes = models.CharField(
        max_length=255,
        blank=True,
        default='',
        help_text="Execution notes or trial details"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp of benchmark execution"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Benchmark Result'
        verbose_name_plural = 'Benchmark Results'

    @property
    def execution_time_ms(self):
        """Returns execution time in milliseconds with 2 decimal precision."""
        return round(self.execution_time_ns / 1_000_000.0, 3)

    @property
    def execution_time_s(self):
        """Returns execution time in seconds with 4 decimal precision."""
        return round(self.execution_time_ns / 1_000_000_000.0, 5)

    @property
    def throughput_ops_per_sec(self):
        """Calculates throughput: records processed per second."""
        secs = self.execution_time_ns / 1_000_000_000.0
        if secs > 0:
            return round(self.dataset_size / secs, 1)
        return 0

    def __str__(self):
        return f"{self.operation} | {self.dataset_size} records | Trial {self.trial_number} | {self.execution_time_ms} ms"
