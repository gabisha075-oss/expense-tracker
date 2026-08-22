from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('landing/', views.landing, name='landing'),
    path('add-income/', views.add_income, name='add_income'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('transactions/', views.transactions, name='transactions'),
    path('budgets/', views.budgets, name='budgets'),
    path('alerts/', views.alerts, name='alerts'),
    path('reports/', views.reports, name='reports'),
    path('download-pdf/', views.download_pdf_report, name='download_pdf'),
    path('edit-income/<int:id>/', views.edit_income, name='edit_income'),
    path('delete-income/<int:id>/', views.delete_income, name='delete_income'),
    path('edit-expense/<int:id>/', views.edit_expense, name='edit_expense'),
    path('delete-expense/<int:id>/', views.delete_expense, name='delete_expense'),
    path('categories/', views.category_management, name='category_management'),
]
