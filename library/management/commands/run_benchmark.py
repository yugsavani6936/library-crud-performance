from django.core.management.base import BaseCommand
from library.benchmark import execute_benchmark_suite

class Command(BaseCommand):
    help = "Runs genuine CRUD performance benchmark evaluation and records results in PostgreSQL"

    def add_arguments(self, parser):
        parser.add_argument('--sizes', nargs='+', type=int, default=[100, 1000], help='Dataset sizes (e.g. 100 1000)')
        parser.add_argument('--trials', type=int, default=3, help='Number of repeated trials')

    def handle(self, *args, **options):
        sizes = options['sizes']
        trials = options['trials']
        ops = ['CREATE', 'READ', 'UPDATE', 'DELETE']

        self.stdout.write(f"Starting benchmark evaluation across scales {sizes} with {trials} trials each...")
        for size in sizes:
            self.stdout.write(f"\n--- Benchmarking Scale: {size} records ---")
            results = execute_benchmark_suite(ops, dataset_size=size, trials=trials)
            for r in results:
                self.stdout.write(f"  [{r.operation}] Trial {r.trial_number}: {r.execution_time_ms} ms ({r.throughput_ops_per_sec} ops/s)")

        self.stdout.write(self.style.SUCCESS(f"\nAll benchmark trials successfully recorded in PostgreSQL!"))
