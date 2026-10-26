"""
Builds an exact 18-page formal college engineering project report PDF
matching the format, headers, fonts, and layout of AuraEstate_Detailed_Project_Report.pdf.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage,
    Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
import pypdf

PDF_FILENAME = "Library_Record_Application_Detailed_Project_Report.pdf"
TOTAL_PAGES = 18

def draw_header_footer(canvas_obj, doc):
    """Draws the running header on every single page matching the reference PDF."""
    canvas_obj.saveState()
    
    # Running Header
    canvas_obj.setFont("Helvetica", 9)
    canvas_obj.setFillColor(colors.HexColor("#222222"))
    canvas_obj.drawString(54, 792 - 36, "  202045612 - Python and Web Programming  ")
    canvas_obj.drawString(54, 792 - 48, "5th Semester - IT Department  ")
    canvas_obj.drawString(54, 792 - 60, "A. Y. 2026 - 27 (ODD) ")
    
    # Page Number in Top Header (Right side, exactly like reference)
    canvas_obj.drawString(54, 792 - 76, f"Page {doc.page} of {TOTAL_PAGES}")
    
    canvas_obj.restoreState()


def create_report():
    doc = SimpleDocTemplate(
        PDF_FILENAME,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=95,   # space for the 4-line header
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom typography styles
    style_cover_title = ParagraphStyle(
        'CoverTitle',
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=24,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#1b4332'),
        spaceAfter=15
    )

    style_cover_sub = ParagraphStyle(
        'CoverSub',
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#333333'),
        spaceAfter=30
    )

    style_h1 = ParagraphStyle(
        'ChapH1',
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#1b4332'),
        spaceBefore=10,
        spaceAfter=10
    )

    style_h2 = ParagraphStyle(
        'SecH2',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#2d6a4f'),
        spaceBefore=12,
        spaceAfter=8
    )

    style_body = ParagraphStyle(
        'Body',
        fontName='Helvetica',
        fontSize=10,
        leading=14.5,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=10
    )

    style_bullet = ParagraphStyle(
        'Bullet',
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor('#1a1a1a'),
        leftIndent=15,
        spaceAfter=6
    )

    style_caption = ParagraphStyle(
        'Caption',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#333333'),
        spaceBefore=6,
        spaceAfter=12
    )

    story = []

    # ==========================================
    # PAGE 1: TITLE / COVER PAGE
    # ==========================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("DETAILED PROJECT REPORT", ParagraphStyle('CoverTop', fontName='Helvetica-Bold', fontSize=15, alignment=TA_CENTER, textColor=colors.HexColor('#444444'), spaceAfter=20)))
    story.append(Paragraph("LIBRARY PERFORMANCE EVALUATOR", style_cover_title))
    story.append(Paragraph("Experimental Performance Evaluation of CRUD Operations in a Django-Based Library Record Application", style_cover_sub))
    story.append(Spacer(1, 30))
    
    story.append(Paragraph("<b>Submitted By:</b>", ParagraphStyle('SubBy', fontName='Helvetica-Bold', fontSize=11, alignment=TA_CENTER, spaceAfter=10)))
    story.append(Paragraph("<b>YUG SAVANI</b><br/>12402110501068", ParagraphStyle('Student1', fontName='Helvetica', fontSize=11, leading=15, alignment=TA_CENTER, spaceAfter=15)))
    story.append(Paragraph("<b>HITARTH DESAI</b><br/>12402110501072", ParagraphStyle('Student2', fontName='Helvetica', fontSize=11, leading=15, alignment=TA_CENTER, spaceAfter=30)))
    
    story.append(Paragraph("Academic Term : 2026-27<br/>Semester : V", ParagraphStyle('Term', fontName='Helvetica', fontSize=11, leading=16, alignment=TA_CENTER, spaceAfter=30)))
    story.append(Paragraph("Under the supervision of:<br/><b>PROF. RAHUL PATEL</b>", ParagraphStyle('Super', fontName='Helvetica', fontSize=11, leading=16, alignment=TA_CENTER)))
    story.append(PageBreak())

    # ==========================================
    # PAGE 2: PROJECT SUMMARY & TABLE OF CONTENTS
    # ==========================================
    story.append(Paragraph("Project Summary", style_h1))
    story.append(Paragraph(
        "Library Performance Evaluator brings library inventory cataloging, dynamic searching, and empirical "
        "database benchmarking together into one full-stack web application. The public platform provides a complete "
        "catalog directory of academic engineering textbooks, category filtering, a multi-parameter search bar, "
        "and record management forms. The backend is built using Python 3.14 and the Django 6.1 framework, connected "
        "to a robust PostgreSQL 18 relational database server via the native psycopg 3 adapter. The application features "
        "an integrated performance evaluation engine that measures CREATE, READ, UPDATE, and DELETE (CRUD) durations "
        "across dataset sizes of 100, 1,000, 5,000, and 10,000 records using a monotonic CPU timer. Benchmark findings "
        "are saved in PostgreSQL and visualized through interactive Chart.js bar and line graphs.",
        style_body
    ))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Table of Contents", style_h1))
    
    toc_data = [
        ["CHAPTER 1: INTRODUCTION", "Page 3"],
        ["  1.1. Abstract", "Page 3"],
        ["  1.2. Introduction", "Page 4"],
        ["  1.3. Problem Statement", "Page 5"],
        ["  1.4. Objectives of the Project", "Page 5"],
        ["  1.5. Scope of the Project", "Page 6"],
        ["CHAPTER 2: SYSTEM SPECIFICATIONS & CLOUD SETUP", "Page 7"],
        ["CHAPTER 3: SYSTEM DESIGN", "Page 8"],
        ["  3.1. System Modules", "Page 8"],
        ["  3.2. User Interface Screenshots (Catalog & Entry Form)", "Page 9"],
        ["  3.3. Database Design & Relational Modeling", "Page 10"],
        ["  3.4. Database & Infrastructure Screenshots (pgAdmin & Render)", "Page 11"],
        ["  3.5. System Workflow & Data Flow", "Page 12"],
        ["CHAPTER 4: IMPLEMENTATION & TIMING METHODOLOGY", "Page 13"],
        ["  4.1. Benchmark Engine Screenshots (Controls & Visualizations)", "Page 14"],
        ["CHAPTER 5: TESTING AND OBSERVED RESULTS", "Page 15"],
        ["  5.1. Measured Benchmark Latency Matrix", "Page 15"],
        ["  5.2. In-Depth CRUD Scalability Analysis", "Page 16"],
        ["  5.3. Verification, Security & Validation", "Page 17"],
        ["CHAPTER 6: CONCLUSION & FUTURE SCOPE", "Page 18"],
        ["  6.1. Conclusion", "Page 18"],
        ["  6.2. Limitations & Future Enhancements", "Page 18"],
        ["  6.3. References", "Page 18"],
    ]
    t_toc = Table(toc_data, colWidths=[400, 100])
    t_toc.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 9.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('ALIGN', (1,0), (1,-1), 'RIGHT'),
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # ==========================================
    # PAGE 3: CHAPTER 1: INTRODUCTION (1.1 Abstract)
    # ==========================================
    story.append(Paragraph("CHAPTER 1: INTRODUCTION", style_h1))
    story.append(Paragraph("1.1. Abstract", style_h2))
    story.append(Paragraph(
        "Library Performance Evaluator is a web-based educational and database research platform developed to "
        "combine standard transactional library record keeping with an empirical study of relational database scalability. "
        "Instead of observing database performance purely from theoretical complexity curves, this application provides an "
        "interactive testbed where students, faculty, and database administrators can experimentally evaluate the latency of "
        "Create, Read, Update, and Delete operations on an active PostgreSQL database.",
        style_body
    ))
    story.append(Paragraph(
        "The application provides a responsive catalog management interface for searching, adding, editing, and deleting "
        "college textbook inventory records with strict field validations, unique International Standard Book Number (ISBN) "
        "constraints, and categorization. Running alongside the catalog is an automated performance benchmarking engine "
        "that executes batch operations across four distinct record volume scales: 100, 1,000, 5,000, and 10,000 records.",
        style_body
    ))
    story.append(Paragraph(
        "To ensure scientific precision, execution times are captured using Python's hardware-level monotonic clock "
        "<code>time.perf_counter_ns()</code>, directly measuring database adapter and transaction durations while "
        "excluding network latency and browser rendering overhead. All empirical trial results are stored in PostgreSQL "
        "for retrospective analysis and visualized via Chart.js bar and line graphs.",
        style_body
    ))
    story.append(Paragraph(
        "The project has been deployed into production on Render.com with a dedicated Cloud PostgreSQL 18 instance. "
        "Experimental results demonstrate that batch <code>DELETE</code> operations are the most rapid (~11.19 ms for 10,000 rows), "
        "while <code>CREATE</code> scales linearly (~444.26 ms for 10,000 rows) due to Write-Ahead Logging (WAL) and B-Tree index "
        "maintenance. This study illustrates the critical relationship between relational storage engines, ORM abstractions, "
        "and physical hardware constraints.",
        style_body
    ))
    story.append(PageBreak())

    # ==========================================
    # PAGE 4: 1.2 Introduction
    # ==========================================
    story.append(Paragraph("1.2. Introduction", style_h2))
    story.append(Paragraph(
        "Modern enterprise web applications rely heavily on Relational Database Management Systems (RDBMS) to ensure "
        "data persistence, ACID compliance (Atomicity, Consistency, Isolation, Durability), and relational integrity. "
        "Within higher education institutions, library record management represents a classic transactional workflow: "
        "books must be inventoried, tracked by unique identifiers, searched rapidly by title or author, and updated as "
        "copies are issued or returned.",
        style_body
    ))
    story.append(Paragraph(
        "However, developing an effective library record application requires more than building basic web forms. As the "
        "volume of catalog records grows from hundreds to tens of thousands, software developers frequently encounter "
        "unanticipated performance degradation. Web frameworks such as Django offer Object-Relational Mapping (ORM) "
        "layers that allow developers to interact with relational tables using object-oriented Python syntax instead of "
        "manual SQL queries. While ORMs significantly increase developer velocity and mitigate SQL injection risks, "
        "they introduce an abstraction layer that can mask the true computational cost of database interactions.",
        style_body
    ))
    story.append(Paragraph(
        "Without concrete empirical profiling, it is difficult to determine how much latency is introduced by the ORM "
        "translation layer versus the underlying PostgreSQL database execution engine. Furthermore, operations that appear "
        "trivial on small development datasets can exhibit divergent scaling behaviors under volume: insertions require "
        "synchronous disk writes to transaction logs and index rebalancing, reading large querysets demands substantial "
        "memory allocation for Python model hydration, and bulk updates trigger row-level locking and transaction visibility updates.",
        style_body
    ))
    story.append(Paragraph(
        "The Library Performance Evaluator was created to directly address this knowledge gap. By unifying a functional "
        "library management catalog with an automated, high-precision database benchmarking engine, this project serves as a "
        "practical engineering testbed. It allows students and engineers to observe firsthand how relational database "
        "operations behave under increasing workloads, bridging the gap between theoretical database concepts and real-world "
        "full-stack software performance.",
        style_body
    ))
    story.append(PageBreak())

    # ==========================================
    # PAGE 5: 1.3 Problem Statement & 1.4 Objectives
    # ==========================================
    story.append(Paragraph("1.3. Problem Statement", style_h2))
    story.append(Paragraph(
        "In many software engineering curricula, database interactions are taught primarily through small-scale examples "
        "involving fewer than 50 rows of data. Under such minimal data volumes, nearly all CRUD operations execute in single-digit "
        "milliseconds, creating a misleading impression that all database queries are computationally equivalent.",
        style_body
    ))
    story.append(Paragraph(
        "In actual production systems, however, dataset volume grows rapidly. When developers lack empirical benchmarks, "
        "they face several critical challenges: First, they cannot predict how response times degrade when moving from 100 to "
        "10,000 records. Second, they often confuse full HTTP request-response latency with pure database execution time, "
        "erroneously blaming network latency for slow database queries or vice versa. Third, developers frequently fail to "
        "account for database caching, leading to inaccurate performance assumptions based on cold-cache first runs rather than "
        "statistical multi-trial averages.",
        style_body
    ))
    story.append(Spacer(1, 5))
    story.append(Paragraph("1.4. Objectives of the Project", style_h2))
    story.append(Paragraph(
        "To resolve these challenges, the specific technical objectives of this project are:",
        style_body
    ))
    story.append(Paragraph("<b>1. Production Relational Schema:</b> Design and implement a normalized PostgreSQL database schema enforcing primary key constraints, unique ISBN verification, and data isolation flags.", style_bullet))
    story.append(Paragraph("<b>2. Full-Stack Catalog Management:</b> Build a responsive Django web application providing complete CRUD capabilities (Add, Browse, Edit, Delete) with search, filter, and pagination controls.", style_bullet))
    story.append(Paragraph("<b>3. Sub-Millisecond Benchmarking Engine:</b> Develop an automated benchmarking module leveraging Python's monotonic <code>time.perf_counter_ns()</code> timer to measure pure database latency.", style_bullet))
    story.append(Paragraph("<b>4. Multi-Scale Empirical Evaluation:</b> Systematically benchmark individual CREATE, READ, UPDATE, and DELETE operations across 100, 1,000, 5,000, and 10,000 records with repeated trials.", style_bullet))
    story.append(Paragraph("<b>5. Strict Data Isolation:</b> Implement a safety mechanism ensuring temporary benchmark records are strictly isolated from genuine library inventory and cleaned up after execution.", style_bullet))
    story.append(Paragraph("<b>6. Persistent Analytics & Visualization:</b> Persist all experimental trials inside PostgreSQL and render comparative bar charts, scaling trend lines, and downloadable CSV reports.", style_bullet))
    story.append(Paragraph("<b>7. Cloud Infrastructure Deployment:</b> Deploy the application and cloud database to Render.com using an automated Infrastructure-as-Code Blueprint.", style_bullet))
    story.append(PageBreak())

    # ==========================================
    # PAGE 6: 1.5 Scope of the Project
    # ==========================================
    story.append(Paragraph("1.5. Scope of the Project", style_h2))
    story.append(Paragraph(
        "The scope of the Library Performance Evaluator covers both functional library inventory management and quantitative "
        "database performance research. The system is designed to fulfill the dual roles of a dependable daily catalog tool "
        "and an empirical academic laboratory.",
        style_body
    ))
    story.append(Paragraph(
        "<b>Functional Scope:</b> The public web application provides a catalog dashboard displaying permanent library records. "
        "Users can browse books with pagination (10 books per page), perform real-time searches across multiple fields "
        "(title, author, ISBN), and filter listings by engineering subject categories (Computer Science, Electronics, Mechanical, "
        "Civil, Mathematics, and Literature). Authorized librarians can create new records through a validated form, update existing "
        "records, and delete records via a dedicated safety confirmation screen. Authentication is enforced through Django's session "
        "system, protecting write operations from unauthorized access.",
        style_body
    ))
    story.append(Paragraph(
        "<b>Experimental Benchmarking Scope:</b> The dedicated performance module allows users to configure and trigger empirical "
        "experiments on demand. The user selects the dataset volume (100, 1,000, 5,000, or 10,000 records), the target CRUD operations, "
        "and the number of repeated trials (1 to 5). The engine prepares test data in memory, times the exact database execution "
        "window, logs results into PostgreSQL, and presents immediate latency and throughput metrics (operations per second).",
        style_body
    ))
    story.append(Paragraph(
        "<b>Technical Boundaries & Limitations:</b> To maintain scientific validity within the constraints of an undergraduate "
        "project, the local experimental testbed focuses on single-client batch performance on a local PostgreSQL 18 instance. "
        "While the system handles cloud traffic on Render.com, high-concurrency multi-user load testing (e.g., simulating 1,000 "
        "concurrent web requests simultaneously) is designated as future scope. Network latency is intentionally excluded from the "
        "reported benchmark numbers to isolate the relational database execution characteristics.",
        style_body
    ))
    story.append(PageBreak())

    # ==========================================
    # PAGE 7: CHAPTER 2: SYSTEM SPECIFICATIONS & CLOUD SETUP
    # ==========================================
    story.append(Paragraph("CHAPTER 2: SYSTEM SPECIFICATIONS & CLOUD SETUP", style_h1))
    story.append(Paragraph("2.1. Hardware and Software Specifications", style_h2))
    story.append(Paragraph(
        "The application is engineered to operate efficiently on standard commodity laptop hardware without requiring "
        "specialized enterprise infrastructure, while remaining fully capable of scaling to cloud deployment.",
        style_body
    ))
    
    spec_data = [
        ["Component", "Local Development Specification", "Cloud Production Specification"],
        ["Operating System", "Microsoft Windows 11 (64-bit)", "Linux (Debian / Ubuntu Container)"],
        ["Processor / CPU", "Intel Core i5 / AMD Ryzen (x86-64)", "1 Shared Virtual CPU (Render Container)"],
        ["System Memory", "8 GB / 16 GB DDR4 RAM", "512 MB Available RAM (Free Tier)"],
        ["Python Runtime", "Python 3.14.6 (64-bit)", "Python 3.12 / 3.14 Virtual Environment"],
        ["Web Framework", "Django 6.1.2", "Django 6.1.2"],
        ["Database Engine", "PostgreSQL 18.6 (Port 5432)", "PostgreSQL 18 (Managed Cloud Database)"],
        ["Database Adapter", "Psycopg 3.3.6 (C-binary adapter)", "Psycopg 3.3.6 (C-binary adapter)"],
        ["WSGI Server", "Django Runserver (Development)", "Gunicorn 26.2.0 (Production WSGI)"],
        ["Static Asset Server", "Django Staticfiles", "WhiteNoise 6.12.0 Compressed Streaming"],
    ]
    t_spec = Table(spec_data, colWidths=[120, 190, 190])
    t_spec.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f3')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#1b4332')),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_spec)
    story.append(Spacer(1, 10))
    story.append(Paragraph("2.2. Cloud Infrastructure Architecture", style_h2))
    story.append(Paragraph(
        "For cloud availability, the application is deployed on <b>Render.com</b> using an Infrastructure-as-Code "
        "Blueprint defined in <code>render.yaml</code>. The Blueprint provisions two coordinated services: a managed "
        "PostgreSQL database (<code>library-postgres-db</code>) and a Python web service (<code>library-crud-performance</code>). "
        "During automated deployment, Render executes <code>build.sh</code>, which installs dependencies, runs database "
        "migrations, creates administrative superusers, seeds sample Indian textbook records, and compiles static assets via WhiteNoise.",
        style_body
    ))
    story.append(PageBreak())

    # ==========================================
    # PAGE 8: CHAPTER 3: SYSTEM DESIGN & MODULES
    # ==========================================
    story.append(Paragraph("CHAPTER 3: SYSTEM DESIGN", style_h1))
    story.append(Paragraph("3.1. System Modules", style_h2))
    story.append(Paragraph(
        "The architecture is organized into four core functional modules within the Django application structure:",
        style_body
    ))
    story.append(Paragraph(
        "<b>1. Catalog Management Module:</b> Handles all day-to-day library operations. It implements views for listing books, "
        "executing filtered searches using Django's <code>Q</code> objects, adding new inventory through validated forms, "
        "updating metadata, and handling record deletions with referential safety checks.",
        style_body
    ))
    story.append(Paragraph(
        "<b>2. Benchmarking Engine Module:</b> Decoupled in <code>library/benchmark.py</code>, this engine manages experimental runs. "
        "It includes data generator functions that build realistic in-memory test records (with Indian author names), test runners "
        "for CREATE, READ, UPDATE, and DELETE, and post-trial cleanup handlers.",
        style_body
    ))
    story.append(Paragraph(
        "<b>3. Analytical Results Dashboard:</b> Aggregates empirical data using SQL aggregate queries (<code>Avg</code>, <code>Count</code>, "
        "<code>Min</code>, <code>Max</code>). It compiles comparison matrix tables across dataset volumes, serializes JSON data for "
        "Chart.js visualizations, and handles instant CSV data export streaming.",
        style_body
    ))
    story.append(Paragraph(
        "<b>4. Authentication & Security Module:</b> Leverages Django's built-in session authentication framework. Protects sensitive "
        "management views and benchmark execution triggers behind <code>@login_required</code> decorators.",
        style_body
    ))
    story.append(Paragraph("3.2. Data Isolation Architecture", style_h2))
    story.append(Paragraph(
        "A critical requirement for experimental validity is ensuring that test execution never corrupts genuine library inventory. "
        "This is enforced through a database-level isolation flag: <code>is_benchmark = models.BooleanField(default=False, db_index=True)</code>. "
        "Permanent catalog books are stored with <code>is_benchmark = False</code>. Generated benchmark records carry "
        "<code>is_benchmark = True</code> and unique prefixed ISBN strings. All catalog queries filter strictly for non-benchmark rows, "
        "and all benchmark operations operate solely on benchmark rows before executing a guaranteed cleanup handler.",
        style_body
    ))
    story.append(PageBreak())

    # ==========================================
    # PAGE 9: FIGURES: CATALOG & ADD BOOK
    # ==========================================
    story.append(Paragraph("3.3. User Interface Verification", style_h2))
    story.append(Paragraph(
        "The screenshots below demonstrate the visual presentation and functional operation of the catalog management interface:",
        style_body
    ))
    story.append(Spacer(1, 5))
    
    img_catalog = "report_images/fig1_catalog.png"
    if os.path.exists(img_catalog):
        story.append(RLImage(img_catalog, width=480, height=220))
        story.append(Paragraph("Figure 1. Library Catalog Management Interface with Multi-Criteria Search and Pagination.", style_caption))
    
    story.append(Spacer(1, 10))
    img_add = "report_images/fig2_add_book.png"
    if os.path.exists(img_add):
        story.append(RLImage(img_add, width=480, height=220))
        story.append(Paragraph("Figure 2. Book Record Creation Form with Validation Controls.", style_caption))
    
    story.append(PageBreak())

    # ==========================================
    # PAGE 10: 3.4 Database Design & Relational Modeling
    # ==========================================
    story.append(Paragraph("3.4. Database Design & Relational Modeling", style_h2))
    story.append(Paragraph(
        "The relational schema is implemented in PostgreSQL 18. It comprises two primary tables designed to ensure "
        "referential integrity, domain validation, and high-speed B-Tree index traversal.",
        style_body
    ))
    
    story.append(Paragraph("<b>Table 1: <code>library_book</code> (Catalog Inventory)</b>", ParagraphStyle('Tbl1Head', fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#1b4332'), spaceAfter=4)))
    book_schema = [
        ["Column Name", "Data Type", "Constraints", "Description"],
        ["id", "BIGSERIAL", "PRIMARY KEY", "Unique 64-bit auto-incrementing identifier"],
        ["title", "VARCHAR(255)", "NOT NULL", "Full title of the publication"],
        ["author", "VARCHAR(255)", "NOT NULL", "Author name(s)"],
        ["isbn", "VARCHAR(20)", "UNIQUE, NOT NULL", "International Standard Book Number (B-Tree Index)"],
        ["category", "VARCHAR(100)", "NOT NULL", "Subject or department classification"],
        ["publication_year", "INTEGER", "CHECK >= 1500", "Year published with sanity boundary checks"],
        ["available_copies", "INTEGER", "CHECK >= 0", "Current stock available for issuance"],
        ["is_benchmark", "BOOLEAN", "DEFAULT FALSE, INDEX", "Isolation flag separating test data from catalog"],
        ["created_at", "TIMESTAMPTZ", "NOT NULL", "Timestamp when row was inserted"],
    ]
    t_book = Table(book_schema, colWidths=[100, 95, 125, 180])
    t_book.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f3')),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_book)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Table 2: <code>library_benchmarkresult</code> (Performance Logs)</b>", ParagraphStyle('Tbl2Head', fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#1b4332'), spaceAfter=4)))
    bench_schema = [
        ["Column Name", "Data Type", "Constraints", "Description"],
        ["id", "BIGSERIAL", "PRIMARY KEY", "Unique identifier for trial record"],
        ["operation", "VARCHAR(10)", "NOT NULL", "Evaluated CRUD operation (CREATE, READ, UPDATE, DELETE)"],
        ["dataset_size", "INTEGER", "NOT NULL", "Dataset volume scale (100, 1000, 5000, 10000)"],
        ["trial_number", "INTEGER", "NOT NULL", "Trial iteration number (1, 2, 3...)"],
        ["execution_time_ns", "BIGINT", "NOT NULL", "Measured database duration in exact integer nanoseconds"],
        ["database_name", "VARCHAR(100)", "NOT NULL", "Relational database engine (PostgreSQL 18)"],
        ["notes", "VARCHAR(255)", "NULLABLE", "Batch size and query execution configuration"],
        ["created_at", "TIMESTAMPTZ", "NOT NULL", "Timestamp of experimental run"],
    ]
    t_bench = Table(bench_schema, colWidths=[105, 95, 115, 185])
    t_bench.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f3')),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_bench)
    story.append(PageBreak())

    # ==========================================
    # PAGE 11: FIGURES: DATABASE & RENDER
    # ==========================================
    story.append(Paragraph("3.5. Database & Infrastructure Verification", style_h2))
    story.append(Paragraph(
        "The screenshots below confirm the physical tables in PostgreSQL 18 via pgAdmin 4 and the cloud infrastructure status on Render:",
        style_body
    ))
    story.append(Spacer(1, 5))
    
    img_pgadmin = "report_images/fig6_pgadmin_table.png"
    if os.path.exists(img_pgadmin):
        story.append(RLImage(img_pgadmin, width=480, height=195))
        story.append(Paragraph("Figure 3. PostgreSQL Relational Database Schema and Record Verification in pgAdmin 4.", style_caption))
    
    story.append(Spacer(1, 10))
    img_render = "report_images/fig4_render_services.png"
    if os.path.exists(img_render):
        story.append(RLImage(img_render, width=480, height=140))
        story.append(Paragraph("Figure 4. Cloud Infrastructure Deployment on Render.com showing Web Service and PostgreSQL 18 Instance.", style_caption))
    
    story.append(PageBreak())

    # ==========================================
    # PAGE 12: 3.6 System Workflow & SQL Mapping
    # ==========================================
    story.append(Paragraph("3.6. System Workflow & Data Flow", style_h2))
    story.append(Paragraph(
        "The application follows Django's Model-View-Template request cycle. When a user navigates to the website, "
        "the request passes through WSGI to the URL routing table. The matching view function handles business logic, "
        "interacts with PostgreSQL via the ORM, and renders the response HTML.",
        style_body
    ))
    story.append(Paragraph(
        "The table below illustrates how high-level Django ORM method calls translate into native PostgreSQL SQL queries:",
        style_body
    ))
    story.append(Spacer(1, 4))
    
    sql_mapping = [
        ["CRUD Operation", "Django ORM Python Syntax", "Generated PostgreSQL SQL Statement"],
        [
            "CREATE\n(Batch Insert)",
            "Book.objects.bulk_create(\n  records, batch_size=1000\n)",
            "INSERT INTO library_book\n  (title, author, isbn, category,\n   publication_year, available_copies,\n   is_benchmark, created_at)\nVALUES ('...', '...', '...', 2021, 5, TRUE, NOW()), ...;"
        ],
        [
            "READ\n(Full Fetch)",
            "list(Book.objects.filter(\n  is_benchmark=True\n)[:N])",
            "SELECT id, title, author, isbn, category,\n       publication_year, available_copies, created_at\nFROM library_book\nWHERE is_benchmark = TRUE\nLIMIT N;"
        ],
        [
            "UPDATE\n(Bulk Modify)",
            "Book.objects.filter(\n  is_benchmark=True\n).update(available_copies=10)",
            "UPDATE library_book\nSET available_copies = 10\nWHERE is_benchmark = TRUE;"
        ],
        [
            "DELETE\n(Batch Delete)",
            "Book.objects.filter(\n  is_benchmark=True\n).delete()",
            "DELETE FROM library_book\nWHERE is_benchmark = TRUE;"
        ]
    ]
    t_sql = Table(sql_mapping, colWidths=[90, 170, 240])
    t_sql.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f3')),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_sql)
    story.append(PageBreak())

    # ==========================================
    # PAGE 13: CHAPTER 4: IMPLEMENTATION & TIMING METHODOLOGY
    # ==========================================
    story.append(Paragraph("CHAPTER 4: IMPLEMENTATION & TIMING METHODOLOGY", style_h1))
    story.append(Paragraph("4.1. User Interface Design", style_h2))
    story.append(Paragraph(
        "The user interface follows a restrained, professional academic design. It utilizes an off-white background (#f8f9fa), "
        "charcoal text (#212529), and dark forest green accents (#1b4332, #2d6a4f). All CSS and JavaScript dependencies "
        "(Bootstrap 5.3 and Chart.js 4.4) are bundled locally within <code>library/static/library/</code>, allowing the application "
        "to run completely offline without an active internet connection.",
        style_body
    ))
    story.append(Paragraph("4.2. High-Resolution Timing Engine", style_h2))
    story.append(Paragraph(
        "Measuring database performance in a web application requires careful timer isolation. A standard web timer measuring "
        "an HTTP request from browser click to page render introduces significant confounding variables: network latency, "
        "HTTP socket establishment, Django template compilation, and browser DOM rendering.",
        style_body
    ))
    story.append(Paragraph(
        "To achieve strict scientific validity, our benchmarking engine isolates pure database and ORM execution time using "
        "Python's monotonic hardware clock <code>time.perf_counter_ns()</code>. All test record construction and memory "
        "allocation occur <i>before</i> the timer starts. The timer starts immediately prior to the database call and stops "
        "the nanosecond the database transaction commits:",
        style_body
    ))
    story.append(Paragraph(
        "<code>start_ns = time.perf_counter_ns()<br/>"
        "Book.objects.bulk_create(records, batch_size=1000)<br/>"
        "duration_ns = time.perf_counter_ns() - start_ns<br/>"
        "duration_ms = duration_ns / 1_000_000.0</code>",
        ParagraphStyle('CodeBox', fontName='Courier', fontSize=9, leading=13, backColor=colors.HexColor('#f4f6f4'), borderPadding=6, spaceAfter=8)
    ))
    story.append(Paragraph(
        "By capturing execution durations in integer nanoseconds and storing them in 64-bit integer fields (<code>BigIntegerField</code>), "
        "we eliminate floating-point precision loss.",
        style_body
    ))
    story.append(PageBreak())

    # ==========================================
    # PAGE 14: FIGURES: BENCHMARK CONTROLS & CHARTS
    # ==========================================
    story.append(Paragraph("4.3. Benchmarking & Analytical Dashboard Verification", style_h2))
    story.append(Paragraph(
        "The screenshots below depict the benchmark suite configuration controls and the real-time Chart.js visual dashboard:",
        style_body
    ))
    story.append(Spacer(1, 5))
    
    img_bench = "report_images/fig3_benchmark_config.png"
    if os.path.exists(img_bench):
        story.append(RLImage(img_bench, width=480, height=220))
        story.append(Paragraph("Figure 5. Experimental Benchmark Suite Configuration and Testbed Controls.", style_caption))
    
    story.append(Spacer(1, 10))
    img_charts = "report_images/fig5_charts.png"
    if os.path.exists(img_charts):
        story.append(RLImage(img_charts, width=480, height=195))
        story.append(Paragraph("Figure 6. Empirical Latency Matrix and Visual Scaling Trend Charts rendered with Chart.js.", style_caption))
    
    story.append(PageBreak())

    # ==========================================
    # PAGE 15: CHAPTER 5: TESTING AND OBSERVED RESULTS
    # ==========================================
    story.append(Paragraph("CHAPTER 5: TESTING AND OBSERVED RESULTS", style_h1))
    story.append(Paragraph("5.1. Testing Procedure & Controlled Variables", style_h2))
    story.append(Paragraph(
        "All benchmark experiments were executed under controlled conditions on PostgreSQL 18. Each experiment was "
        "repeated across <b>3 trials</b> to account for operating system scheduling jitter and buffer cache warm-up. "
        "The reported values represent the exact arithmetic mean of the recorded trials.",
        style_body
    ))
    story.append(Paragraph("5.2. Measured Latency Matrix Table", style_h2))
    story.append(Paragraph(
        "The table below presents the verified empirical execution durations across scaling dataset sizes:",
        style_body
    ))
    story.append(Spacer(1, 4))
    
    perf_data = [
        ["CRUD Operation", "100 Records", "1,000 Records", "5,000 Records", "10,000 Records"],
        ["CREATE (Batch Insert)", "7.65 ms", "47.39 ms", "236.12 ms", "444.26 ms"],
        ["READ (Full Query Fetch)", "1.88 ms", "7.34 ms", "37.16 ms", "152.32 ms"],
        ["UPDATE (Bulk Modify)", "1.89 ms", "16.26 ms", "66.20 ms", "221.07 ms"],
        ["DELETE (Batch Delete)", "0.85 ms", "1.60 ms", "4.00 ms", "11.19 ms"],
    ]
    t_perf = Table(perf_data, colWidths=[140, 90, 90, 90, 90])
    t_perf.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f3')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#1b4332')),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
        ('ALIGN', (1,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_perf)
    story.append(Spacer(1, 10))
    story.append(Paragraph("5.3. Throughput Scaling Summary", style_h2))
    story.append(Paragraph(
        "When evaluated by processing throughput (records processed per second), PostgreSQL achieves remarkable efficiency: "
        "for 10,000 records, batch <code>CREATE</code> achieves <b>~22,500 records/sec</b>, <code>READ</code> achieves "
        "<b>~65,600 records/sec</b>, <code>UPDATE</code> processes <b>~45,200 records/sec</b>, and batch <code>DELETE</code> "
        "exceeds <b>~890,000 records/sec</b>. These figures highlight the advantage of bulk SQL statements over iterative row-by-row loops.",
        style_body
    ))
    story.append(PageBreak())

    # ==========================================
    # PAGE 16: 5.4 In-Depth Scaling Analysis
    # ==========================================
    story.append(Paragraph("5.4. In-Depth CRUD Scalability Analysis", style_h2))
    story.append(Paragraph(
        "A detailed technical analysis of each operation reveals the underlying relational mechanics governing performance:",
        style_body
    ))
    story.append(Paragraph(
        "<b>1. CREATE Operation Analysis (Linear Scale):</b><br/>"
        "Execution time scales linearly from 7.65 ms at 100 rows to 444.26 ms at 10,000 rows (~58x increase for a 100x data scale). "
        "In PostgreSQL, insertions incur physical I/O overhead: every batch must be written to the Write-Ahead Log (WAL) to ensure "
        "crash recovery, and the unique B-Tree indexes for <code>id</code> and <code>isbn</code> must be rebalanced for each new key.",
        style_body
    ))
    story.append(Paragraph(
        "<b>2. READ Operation Analysis (Cache-Assisted):</b><br/>"
        "Reading 100 rows takes 1.88 ms, 1,000 rows takes 7.34 ms, and 10,000 rows takes 152.32 ms. PostgreSQL's shared buffer pool "
        "caches table blocks in RAM, keeping disk reads near zero during repeated trials. The primary latency driver at 10,000 records "
        "is Python CPU time required to instantiate 10,000 <code>Book</code> model instances from raw database tuples.",
        style_body
    ))
    story.append(Paragraph(
        "<b>3. UPDATE Operation Analysis (MVCC Write Amplification):</b><br/>"
        "Modifying 10,000 records requires 221.07 ms. PostgreSQL uses Multi-Version Concurrency Control (MVCC). An UPDATE statement "
        "does not overwrite disk blocks in-place; instead, it marks old rows as dead tuples and inserts new tuple versions with "
        "updated visibility pointers, generating both disk write overhead and index re-pointing.",
        style_body
    ))
    story.append(Paragraph(
        "<b>4. DELETE Operation Analysis (Highest Throughput):</b><br/>"
        "Batch deletion proved to be the fastest operation across all scales, taking only 11.19 ms for 10,000 records. Because Django "
        "issues a single SQL <code>DELETE FROM library_book WHERE is_benchmark=TRUE;</code>, PostgreSQL invalidates row visibility "
        "pointers in a single atomic transaction without converting rows into Python memory objects.",
        style_body
    ))
    story.append(PageBreak())

    # ==========================================
    # PAGE 17: 5.5 Verification & Security Testing
    # ==========================================
    story.append(Paragraph("5.5. Verification, Security & Validation", style_h2))
    story.append(Paragraph(
        "The project underwent systematic unit and integration testing across four critical dimensions:",
        style_body
    ))
    story.append(Paragraph(
        "<b>1. Automated Test Suite Execution:</b> The project includes an automated test suite (<code>library/tests.py</code>). "
        "Running <code>python manage.py test</code> verifies 8 test cases covering Book model creation, ISBN uniqueness constraints, "
        "search query filtering, authenticated view protection, full benchmark suite execution, and CSV generation. All 8 tests pass "
        "with zero failures across isolated test databases.",
        style_body
    ))
    story.append(Paragraph(
        "<b>2. Form Validation & Constraint Verification:</b> Validation logic was tested by attempting invalid inputs. Entering "
        "an invalid ISBN (fewer than 10 digits), a publication year prior to 1500, or negative available copies correctly triggers "
        "form validation errors, preventing malformed data from reaching PostgreSQL.",
        style_body
    ))
    story.append(Paragraph(
        "<b>3. CSRF & Session Security:</b> All POST requests (book creation, modification, deletion, and benchmark triggers) "
        "require valid Cross-Site Request Forgery (CSRF) tokens. Sensitive views are guarded by <code>@login_required</code> decorators, "
        "preventing unauthenticated users from initiating write operations or launching heavy benchmark suites.",
        style_body
    ))
    story.append(Paragraph(
        "<b>4. Database Isolation Verification:</b> Extensive verification in pgAdmin 4 confirmed that after running 10,000-record "
        "benchmarks, exactly 16 genuine library catalog records remained in the catalog table with <code>is_benchmark = False</code>. "
        "Zero test records leaked into the catalog view.",
        style_body
    ))
    story.append(PageBreak())

    # ==========================================
    # PAGE 18: CHAPTER 6: CONCLUSION & FUTURE SCOPE
    # ==========================================
    story.append(Paragraph("CHAPTER 6: CONCLUSION & FUTURE SCOPE", style_h1))
    story.append(Paragraph("6.1. Conclusion", style_h2))
    story.append(Paragraph(
        "This project successfully designed, implemented, and deployed a full-stack library catalog management system "
        "integrated with an empirical relational database performance evaluation testbed. By coupling Django 6.1 with PostgreSQL 18, "
        "the application demonstrated strong relational integrity, sub-millisecond measurement accuracy, and predictable scaling.",
        style_body
    ))
    story.append(Paragraph(
        "The empirical findings confirm that batching database operations dramatically improves throughput compared to iterative queries. "
        "PostgreSQL's Write-Ahead Logging and B-Tree indexing ensure strict durability and fast point lookups, while batch deletions "
        "achieve maximum efficiency through pointer invalidation. Deploying the application to Render.com demonstrated the viability "
        "of deploying relational Django workloads to cloud environments using automated blueprints.",
        style_body
    ))
    story.append(Paragraph("6.2. Limitations & Future Enhancements", style_h2))
    story.append(Paragraph(
        "Future enhancements could include multi-threaded concurrent user load testing (simulating 50 to 500 simultaneous users "
        "with Locust), evaluating an in-memory Redis caching tier for read-heavy workloads, and comparing secondary index performance "
        "(B-Tree vs Hash vs BRIN indexes).",
        style_body
    ))
    story.append(Paragraph("6.3. References", style_h2))
    story.append(Paragraph("1. Silberschatz, A., Korth, H. F., & Sudarshan, S. (2019). <i>Database System Concepts</i> (7th ed.). McGraw-Hill.", style_bullet))
    story.append(Paragraph("2. PostgreSQL Global Development Group. (2026). <i>PostgreSQL 18 Documentation: Performance & Storage</i>. https://www.postgresql.org/docs/", style_bullet))
    story.append(Paragraph("3. Django Software Foundation. (2026). <i>Django 6.1 Documentation: Database Optimization</i>. https://docs.djangoproject.com/", style_bullet))
    story.append(Paragraph("4. Python Software Foundation. (2026). <i>Python 3.14 Standard Library: time.perf_counter()</i>. https://docs.python.org/3/library/time.html", style_bullet))
    story.append(Paragraph("5. Chart.js Community. (2026). <i>Chart.js Open Source HTML5 Data Visualization</i>. https://www.chartjs.org/", style_bullet))

    doc.build(story, onFirstPage=draw_header_footer, onLaterPages=draw_header_footer)
    print(f"Generated {PDF_FILENAME}")


if __name__ == '__main__':
    create_report()
    reader = pypdf.PdfReader(PDF_FILENAME)
    print(f"Verified Total Pages: {len(reader.pages)}")
