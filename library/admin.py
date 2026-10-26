from django.contrib import admin
from .models import Book, BenchmarkResult

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'isbn', 'category', 'publication_year', 'available_copies', 'is_benchmark', 'created_at')
    list_filter = ('category', 'is_benchmark', 'publication_year')
    search_fields = ('title', 'author', 'isbn')
    ordering = ('-created_at',)
    list_per_page = 20

@admin.register(BenchmarkResult)
class BenchmarkResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'operation', 'dataset_size', 'trial_number', 'execution_time_ms', 'throughput_ops_per_sec', 'database_name', 'created_at')
    list_filter = ('operation', 'dataset_size', 'database_name')
    search_fields = ('operation', 'database_name', 'notes')
    ordering = ('-created_at',)
    list_per_page = 25
