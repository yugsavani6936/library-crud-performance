# Experimental Performance Evaluation of CRUD Operations in a Django-Based Library Record Application

A full-stack college engineering capstone project designed to manage library book records and experimentally evaluate the relational performance of **CREATE**, **READ**, **UPDATE**, and **DELETE** (CRUD) operations across scaling dataset volumes (100, 1,000, 5,000, and 10,000 records) in **PostgreSQL 18**.

---

## 1. Project Overview & Architecture

- **Backend:** Django 6.1 (Python 3.14.6)
- **Database:** PostgreSQL 18 (Relational DBMS running on port 5432)
- **Database Driver:** `psycopg` 3.3.6 (C-binary adapter)
- **Timer Engine:** Python monotonic `time.perf_counter_ns()`
- **Frontend:** HTML5, CSS3, Bootstrap 5 (Local offline bundle), Chart.js 4.4 (Local offline bundle)
- **Database Inspection Tool:** pgAdmin 4

```
                               +-----------------------------+
                               |     Web Browser (Chrome)    |
                               +-----------------------------+
                                              |
                                   HTTP GET / POST Requests
                                              |
                                              v
+-----------------------------------------------------------------------------------------+
|                                    Django Web Application                               |
|                                                                                         |
|  +--------------------+   +-----------------------+   +------------------------------+  |
|  | Catalog Management |   | Performance Benchmark |   |      Results Dashboard       |  |
|  |     (views.py)     |   |     (benchmark.py)    |   |     (Chart.js + CSV Export)  |  |
|  +--------------------+   +-----------------------+   +------------------------------+  |
|            |                          |                               |                 |
|            +--------------------------+-------------------------------+                 |
|                                       |                                                 |
|                        Django ORM (Object-Relational Mapping)                           |
+-----------------------------------------------------------------------------------------+
                                        |
                             SQL Queries via psycopg 3
                                        |
                                        v
+-----------------------------------------------------------------------------------------+
|                                PostgreSQL 18 Database Server                            |
|                                                                                         |
|      +--------------------------------+       +----------------------------------+      |
|      |          library_book          |       |     library_benchmarkresult      |      |
|      |--------------------------------|       |----------------------------------|      |
|      | id (PK, BigInt)                |       | id (PK, BigInt)                  |      |
|      | title (VarChar)                |       | operation (VarChar)              |      |
|      | author (VarChar)               |       | dataset_size (Int)               |      |
|      | isbn (VarChar, UNIQUE)         |       | trial_number (Int)               |      |
|      | category (VarChar)             |       | execution_time_ns (BigInt)       |      |
|      | publication_year (Int)         |       | database_name (VarChar)          |      |
|      | available_copies (Int)         |       | notes (VarChar)                  |      |
|      | is_benchmark (Boolean, INDEX)  |       | created_at (Timestamp)           |      |
|      | created_at (Timestamp)         |       +----------------------------------+      |
|      +--------------------------------+                                                 |
+-----------------------------------------------------------------------------------------+
```

---

## 2. Directory Structure

```text
python library record application/
├── config/                     # Django project core configuration
│   ├── settings.py             # PostgreSQL connection, static files, auth
│   ├── urls.py                 # Root URL router
│   ├── wsgi.py
│   └── asgi.py
├── library/                    # Main application package
│   ├── models.py               # Book & BenchmarkResult relational models
│   ├── views.py                # CRUD views, benchmarking runner, CSV export
│   ├── forms.py                # BookForm with validation (ISBN, year, copies)
│   ├── urls.py                 # Application routes
│   ├── admin.py                # Django admin configuration
│   ├── benchmark.py            # High-resolution benchmark timing engine
│   ├── tests.py                # Automated unit & integration tests
│   ├── management/
│   │   └── commands/
│   │       ├── seed_books.py   # Populates library with Indian textbook records
│   │       └── run_benchmark.py# CLI benchmark runner
│   ├── templates/library/      # Frontend templates
│   │   ├── base.html           # Master layout with dark green theme
│   │   ├── book_list.html      # Book catalog with search & pagination
│   │   ├── book_form.html      # Add & Edit book form
│   │   ├── book_confirm_delete.html # Confirmation modal before deletion
│   │   ├── benchmark.html      # Interactive benchmark execution interface
│   │   ├── results.html        # Matrix table & offline Chart.js graphs
│   │   ├── methodology.html    # Academic methodology & viva preparation
│   │   └── login.html          # Authentication page with demo credentials
│   └── static/library/         # 100% Offline Static Assets
│       ├── css/
│       │   ├── bootstrap.min.css
│       │   └── custom.css      # Dark green & charcoal academic palette
│       └── js/
│           ├── bootstrap.bundle.min.js
│           └── chart.umd.min.js
├── manage.py                   # Django CLI utility
├── requirements.txt            # Python dependencies
├── .env                        # Local database credentials
├── .env.example                # Safe environment variable template
├── .gitignore                  # Git exclusions
└── README.md                   # Full documentation & viva guide
```

---

## 3. Quick Start Setup Guide (Windows)

### Step 1: Clone or Navigate to the Folder
Open PowerShell or Command Prompt in the project folder:
```powershell
cd "c:\Users\yugsa\Downloads\python library record application"
```

### Step 2: Activate the Virtual Environment
```powershell
.\venv\Scripts\activate
```

### Step 3: Verify Environment Configuration (`.env`)
The `.env` file is already pre-configured for your local PostgreSQL service:
```ini
DEBUG=True
SECRET_KEY=django-insecure-lib-eval-perf-counter-academic-2026-key
DB_NAME=library_db
DB_USER=postgres
DB_PASSWORD=yug
DB_HOST=localhost
DB_PORT=5432
```

### Step 4: Run Migrations and Verify Database
```powershell
.\venv\Scripts\python.exe manage.py migrate
```

### Step 5: Start the Development Server
```powershell
.\venv\Scripts\python.exe manage.py runserver
```

Open Google Chrome and navigate to:
```
http://127.0.0.1:8000/
```

---

## 4. Default Demo Credentials

For live demonstration to faculty and examiners:
- **Username:** `admin`
- **Password:** `admin123`

The application allows unauthenticated users to view the catalog and results, while write operations (Add/Edit/Delete books, running benchmarks, clearing history, CSV export) are protected by Django authentication.

---

## 5. Live Demonstration Guide

### Feature 1: Library Catalog Management
1. Navigate to **Catalog Management** (`http://127.0.0.1:8000/`).
2. Search for textbooks by title (e.g., `Mathematics`), author (`Grewal`), or ISBN (`978-8174091955`).
3. Click **Add New Book** to insert a new textbook.
4. Click **Edit** to update available copies or publication details.
5. Click **Delete** to view the confirmation dialog and verify row deletion.

### Feature 2: Running Performance Benchmarks
1. Navigate to **Performance Tests** (`http://127.0.0.1:8000/benchmark/`).
2. Select a dataset size (e.g., `100`, `1,000`, or `10,000` records).
3. Select which CRUD operations to measure (`CREATE`, `READ`, `UPDATE`, `DELETE`).
4. Select the number of repeated trials (e.g. `3 Trials`).
5. Click **Run Benchmark Experiment**.
6. The high-resolution timer (`time.perf_counter_ns()`) executes the operations against PostgreSQL, records the result in the database, and displays the execution time in milliseconds and throughput in operations/second.

### Feature 3: Viewing Results & Visual Charts
1. Navigate to **Results Dashboard** (`http://127.0.0.1:8000/results/`).
2. Observe the **Average Execution Time Matrix** comparing operations across dataset sizes.
3. Inspect the **Comparative Bar Chart** and **Scaling Trend Line Chart** rendered via Chart.js.
4. Click **Export CSV Dataset** to download all recorded empirical measurements in CSV format.

### Running Benchmarks from Command Line (CLI)
You can also run benchmarks directly in the terminal:
```powershell
.\venv\Scripts\python.exe manage.py run_benchmark --sizes 100 1000 5000 10000 --trials 3
```

To re-seed sample books:
```powershell
.\venv\Scripts\python.exe manage.py seed_books
```

To run all automated tests:
```powershell
.\venv\Scripts\python.exe manage.py test
```

---

## 6. How to View Tables & Records in pgAdmin 4

1. Launch **pgAdmin 4** from your Windows Start Menu.
2. In the left sidebar (*Object Explorer*), expand:
   - **Servers** &rarr; **PostgreSQL 18** (enter master password: `yug` when prompted).
   - **Databases** &rarr; **`library_db`**.
   - **Schemas** &rarr; **public** &rarr; **Tables**.
3. Right-click on **`library_book`** &rarr; Select **View/Edit Data** &rarr; **All Rows**.
   - You will see all catalog books with author names (Dr. B.S. Grewal, Dr. N.P. Bali, etc.).
4. Right-click on **`library_benchmarkresult`** &rarr; Select **View/Edit Data** &rarr; **All Rows**.
   - You will see every empirical benchmark trial with exact `execution_time_ns` and notes.

You can also run manual SQL queries in the pgAdmin Query Tool:
```sql
-- View average CRUD execution times grouped by dataset size
SELECT 
    operation, 
    dataset_size, 
    COUNT(*) AS trial_count, 
    ROUND(AVG(execution_time_ns) / 1000000.0, 3) AS avg_duration_ms
FROM library_benchmarkresult
GROUP BY operation, dataset_size
ORDER BY dataset_size ASC, operation ASC;
```

---

## 7. College Viva Voce Preparation Guide

### Q1: What is Django?
**Answer:** Django is a high-level, open-source Python web framework based on the Model-View-Template (MVT) architecture. It allows developers to build secure, database-driven web applications rapidly by providing an Object-Relational Mapper (ORM), built-in authentication, form validation, and URL routing out of the box.

### Q2: What is PostgreSQL?
**Answer:** PostgreSQL is an advanced, enterprise-class, open-source Object-Relational Database Management System (ORDBMS). It runs as an independent server process, provides ACID transaction guarantees, supports complex data types, and utilizes Multi-Version Concurrency Control (MVCC) for high-performance concurrent operations.

### Q3: What is a Relational Database?
**Answer:** A relational database organizes data into structured tables consisting of rows (records) and columns (attributes). Tables are interconnected through foreign keys and relational constraints. It enforces schema rules, data integrity, and supports the Structured Query Language (SQL).

### Q4: What are CRUD Operations?
**Answer:** CRUD stands for:
- **Create:** Inserting new records into a database (`INSERT` in SQL).
- **Read:** Querying and retrieving existing records (`SELECT` in SQL).
- **Update:** Modifying attribute values of existing records (`UPDATE` in SQL).
- **Delete:** Removing records from a table (`DELETE` in SQL).

### Q5: What are Django Models, Views, URLs, and Migrations?
**Answer:**
- **Model:** A Python class that defines the database table schema, fields, and constraints (e.g., `class Book(models.Model)`).
- **View:** A Python function or class that handles incoming HTTP requests, queries models, and returns an HTTP response or renders an HTML template.
- **URL (urls.py):** Maps incoming browser URL patterns to the corresponding view function.
- **Migration:** Django's way of propagating changes made in `models.py` into the physical PostgreSQL database schema (e.g., creating tables or adding columns).

### Q6: What is the purpose of a Primary Key and a Unique Constraint?
**Answer:**
- **Primary Key (PK):** A column (or set of columns) that uniquely identifies every single row in a table. It cannot be NULL (e.g., `id` in `Book`).
- **Unique Constraint:** Guarantees that no two rows have the same value in a specific column (e.g., `isbn` in `Book`). In PostgreSQL, both automatically create a B-Tree index to provide fast lookup performance ($O(\log N)$).

### Q7: How does Django connect to PostgreSQL?
**Answer:** Django connects via the `psycopg` database adapter. The connection parameters (`ENGINE`, `NAME`, `USER`, `PASSWORD`, `HOST`, `PORT`) are defined in `config/settings.py` and read from `.env`. When an ORM operation is called, Django compiles the Python code into a SQL string, sends it across the TCP connection (port 5432) to PostgreSQL, and parses the returned tuples into Python model instances.

### Q8: How is execution time measured in this experiment?
**Answer:** We use Python's `time.perf_counter_ns()`. It provides a monotonic, high-resolution hardware clock unaffected by system clock adjustments. We sample the time immediately before the database call and immediately after completion:
$$\text{Duration (ms)} = \frac{t_{\text{stop}} - t_{\text{start}}}{1\,000\,000}$$
This isolates pure database and ORM processing time from browser-to-server HTTP network latency.

### Q9: Why do we test different dataset sizes (100, 1,000, 10,000)?
**Answer:** Testing across scaling orders of magnitude reveals the scalability characteristics of relational database operations. At small volumes (100 rows), fixed overheads dominate. At larger volumes (10,000 rows), we observe the true linear scaling of bulk inserts, index rebalancing, memory buffer usage, and Write-Ahead Logging (WAL) disk commits.

### Q10: What does Database Indexing mean and how does it affect CRUD performance?
**Answer:** An index is an auxiliary data structure (typically a B-Tree in PostgreSQL) that allows the database engine to locate records without scanning every row in the table (Full Table Scan).
- **Impact on READ:** Dramatically speeds up search queries from $O(N)$ to $O(\log N)$.
- **Impact on CREATE/UPDATE/DELETE:** Slightly slows down write operations because the index data structure must be modified every time a row is added, updated, or removed.

### Q11: What are the limitations of this experimental setup?
**Answer:** Both the Django web server and the PostgreSQL database daemon run on the same physical laptop machine, sharing CPU and RAM. In production enterprise architectures, the web application and database server reside on separate dedicated physical servers connected over a private high-speed network. Additionally, the experiment measures single-client batch throughput rather than high-concurrency multi-user traffic.
