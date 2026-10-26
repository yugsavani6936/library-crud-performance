from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Feature 1: Library Management
    path('', views.book_list, name='book_list'),
    path('books/add/', views.book_create, name='book_create'),
    path('books/<int:pk>/edit/', views.book_update, name='book_update'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),

    # Feature 2: Performance Benchmarking
    path('benchmark/', views.benchmark_view, name='benchmark_view'),

    # Feature 3: Results Dashboard & CSV Export
    path('results/', views.results_dashboard, name='results_dashboard'),
    path('results/export-csv/', views.export_csv, name='export_csv'),
    path('results/clear/', views.clear_benchmarks, name='clear_benchmarks'),

    # Feature 4: Authentication
    path('login/', auth_views.LoginView.as_view(
        template_name='library/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='login'
    ), name='logout'),
]
