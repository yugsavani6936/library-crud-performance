#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install python dependencies
pip install -r requirements.txt

# Collect static files for whitenoise
python manage.py collectstatic --no-input

# Apply database migrations to Cloud PostgreSQL
python manage.py migrate

# Seed sample library books if empty
python manage.py seed_books

# Run initial benchmarks so dashboard has real data
python manage.py run_benchmark --sizes 100 1000 --trials 3
