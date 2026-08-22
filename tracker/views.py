from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST, require_GET
from django.db.models import Sum, Q
from django.utils import timezone
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from decimal import Decimal
import json
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import csv

from .models import Category, Income, Expense, Budget, BudgetAlert, MoneySavingQuote
from .utils import generate_chart_data, check_budget_alerts

@login_required(login_url='login')
def home(request):
    """Home/Dashboard view"""
    today = timezone.now().date()
    current_month = today.month
    current_year = today.year
    
    # Get current month data
    month_start = datetime(current_year, current_month, 1).date()
    if current_month == 12:
        month_end = datetime(current_year + 1, 1, 1).date() - timedelta(days=1)
    else:
        month_end = datetime(current_year, current_month + 1, 1).date() - timedelta(days=1)
    
    # Total income and expense
    total_income = Income.objects.filter(
        user=request.user,
        date__range=[month_start, month_end]
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
    
    total_expense = Expense.objects.filter(
        user=request.user,
        date__range=[month_start, month_end]
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
    
    balance = total_income - total_expense
    
    # Today's transactions
    today_income = Income.objects.filter(
        user=request.user,
        date=today
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
    
    today_expense = Expense.objects.filter(
        user=request.user,
        date=today
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
    
    # Recent transactions
    recent_incomes = Income.objects.filter(user=request.user).order_by('-date')[:5]
    recent_expenses = Expense.objects.filter(user=request.user).order_by('-date')[:5]
    
    # Expense by category (current month)
    expense_by_category = Expense.objects.filter(
        user=request.user,
        date__range=[month_start, month_end]
    ).values('category__name', 'category__emoji', 'category__color').annotate(
        total=Sum('amount')
    ).order_by('-total')
    
    # Unread alerts
    unread_alerts = BudgetAlert.objects.filter(
        user=request.user,
        is_read=False
    ).count()
    
    # Random money saving quote
    quotes = MoneySavingQuote.objects.all()
    quote = quotes.order_by('?').first() if quotes.exists() else None
    
    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'today_income': today_income,
        'today_expense': today_expense,
        'recent_incomes': recent_incomes,
        'recent_expenses': recent_expenses,
        'expense_by_category': expense_by_category,
        'unread_alerts': unread_alerts,
        'quote': quote,
        'current_month': current_month,
        'current_year': current_year,
    }
    
    return render(request, 'home.html', context)

@login_required(login_url='login')
def landing(request):
    """Landing page with overview"""
    return render(request, 'landing.html')

@login_required(login_url='login')
def add_income(request):
    """Add income transaction"""
    if request.method == 'POST':
        category_id = request.POST.get('category')
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        date_str = request.POST.get('date')
        
        try:
            amount = Decimal(amount)
            date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else timezone.now().date()
            
            category = get_object_or_404(Category, id=category_id, user=request.user, category_type='income')
            
            income = Income.objects.create(
                user=request.user,
                category=category,
                amount=amount,
                description=description,
                date=date
            )
            
            messages.success(request, 'Income added successfully!')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'Error adding income: {str(e)}')
    
    categories = Category.objects.filter(user=request.user, category_type='income')
    context = {'categories': categories}
    return render(request, 'add_income.html', context)

@login_required(login_url='login')
def add_expense(request):
    """Add expense transaction"""
    if request.method == 'POST':
        category_id = request.POST.get('category')
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        payment_method = request.POST.get('payment_method', 'Cash')
        date_str = request.POST.get('date')
        
        try:
            amount = Decimal(amount)
            date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else timezone.now().date()
            
            category = get_object_or_404(Category, id=category_id, user=request.user, category_type='expense')
            
            expense = Expense.objects.create(
                user=request.user,
                category=category,
                amount=amount,
                description=description,
                payment_method=payment_method,
                date=date
            )
            
            if 'receipt_image' in request.FILES:
                expense.receipt_image = request.FILES['receipt_image']
                expense.save()
            
            # Check budget alerts
            check_budget_alerts(request.user, category, date)
            
            messages.success(request, 'Expense added successfully!')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'Error adding expense: {str(e)}')
    
    categories = Category.objects.filter(user=request.user, category_type='expense')
    context = {'categories': categories}
    return render(request, 'add_expense.html', context)

@login_required(login_url='login')
def transactions(request):
    """View all transactions"""
    transaction_type = request.GET.get('type', 'all')
    category_filter = request.GET.get('category')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    # Start with base queryset
    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)
    
    # Filter by category
    if category_filter:
        incomes = incomes.filter(category_id=category_filter)
        expenses = expenses.filter(category_id=category_filter)
    
    # Filter by date range
    if date_from:
        date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
        incomes = incomes.filter(date__gte=date_from_obj)
        expenses = expenses.filter(date__gte=date_from_obj)
    
    if date_to:
        date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
        incomes = incomes.filter(date__lte=date_to_obj)
        expenses = expenses.filter(date__lte=date_to_obj)
    
    # Get categories for filter
    categories = Category.objects.filter(user=request.user)
    
    context = {
        'transaction_type': transaction_type,
        'categories': categories,
        'date_from': date_from,
        'date_to': date_to,
        'category_filter': category_filter,
    }
    
    if transaction_type == 'income':
        paginator = Paginator(incomes.order_by('-date'), 20)
        page = request.GET.get('page', 1)
        context['transactions'] = paginator.get_page(page)
    elif transaction_type == 'expense':
        paginator = Paginator(expenses.order_by('-date'), 20)
        page = request.GET.get('page', 1)
        context['transactions'] = paginator.get_page(page)
    else:
        # Combined view (not implemented for pagination)
        context['incomes'] = incomes.order_by('-date')
        context['expenses'] = expenses.order_by('-date')
    
    return render(request, 'transactions.html', context)

@login_required(login_url='login')
def budgets(request):
    """Manage budgets"""
    if request.method == 'POST':
        category_id = request.POST.get('category')
        amount = request.POST.get('amount')
        frequency = request.POST.get('frequency', 'monthly')
        month = request.POST.get('month', timezone.now().month)
        year = request.POST.get('year', timezone.now().year)
        alert_threshold = request.POST.get('alert_threshold', 80)
        
        try:
            category = get_object_or_404(Category, id=category_id, user=request.user, category_type='expense')
            
            Budget.objects.update_or_create(
                user=request.user,
                category=category,
                month=month,
                year=year,
                defaults={
                    'amount': Decimal(amount),
                    'frequency': frequency,
                    'alert_threshold': int(alert_threshold)
                }
            )
            
            messages.success(request, 'Budget saved successfully!')
            return redirect('budgets')
        except Exception as e:
            messages.error(request, f'Error saving budget: {str(e)}')
    
    current_month = timezone.now().month
    current_year = timezone.now().year
    
    # Get current month budgets with spent amount
    budgets_list = []
    for budget in Budget.objects.filter(user=request.user, month=current_month, year=current_year):
        spent = Expense.objects.filter(
            user=request.user,
            category=budget.category,
            date__year=current_year,
            date__month=current_month
        ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
        
        percentage = (spent / budget.amount * 100) if budget.amount > 0 else 0
        budgets_list.append({
            'budget': budget,
            'spent': spent,
            'remaining': budget.amount - spent,
            'percentage': min(int(percentage), 100),
            'status': 'critical' if percentage >= 100 else 'warning' if percentage >= budget.alert_threshold else 'safe'
        })
    
    categories = Category.objects.filter(user=request.user, category_type='expense')
    
    context = {
        'budgets': budgets_list,
        'categories': categories,
        'current_month': current_month,
        'current_year': current_year,
    }
    
    return render(request, 'budgets.html', context)

@login_required(login_url='login')
def alerts(request):
    """View budget alerts"""
    alerts_list = BudgetAlert.objects.filter(user=request.user).order_by('-created_at')
    
    # Mark as read
    if request.method == 'POST':
        alert_id = request.POST.get('alert_id')
        if alert_id == 'all':
            alerts_list.update(is_read=True)
        else:
            alert = get_object_or_404(BudgetAlert, id=alert_id, user=request.user)
            alert.is_read = True
            alert.save()
        return redirect('alerts')
    
    paginator = Paginator(alerts_list, 20)
    page = request.GET.get('page', 1)
    alerts_page = paginator.get_page(page)
    
    context = {'alerts': alerts_page}
    return render(request, 'alerts.html', context)

@login_required(login_url='login')
def reports(request):
    """View reports and analytics"""
    time_range = request.GET.get('range', 'month')
    today = timezone.now().date()
    
    if time_range == 'month':
        start_date = datetime(today.year, today.month, 1).date()
    elif time_range == 'quarter':
        month = today.month
        quarter_month = ((month - 1) // 3) * 3 + 1
        start_date = datetime(today.year, quarter_month, 1).date()
    elif time_range == 'year':
        start_date = datetime(today.year, 1, 1).date()
    else:
        start_date = today - timedelta(days=30)
    
    end_date = today
    
    # Get transactions in range
    incomes = Income.objects.filter(
        user=request.user,
        date__range=[start_date, end_date]
    )
    expenses = Expense.objects.filter(
        user=request.user,
        date__range=[start_date, end_date]
    )
    
    total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
    total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
    
    # Expense by category
    expense_by_category = expenses.values('category__name', 'category__emoji', 'category__color').annotate(
        total=Sum('amount')
    ).order_by('-total')
    
    # Income by category
    income_by_category = incomes.values('category__name', 'category__emoji', 'category__color').annotate(
        total=Sum('amount')
    ).order_by('-total')
    
    # Prepare chart data
    chart_data = {
        'expense_labels': [item['category__name'] for item in expense_by_category],
        'expense_data': [float(item['total']) for item in expense_by_category],
        'expense_colors': [item['category__color'] for item in expense_by_category],
        'income_labels': [item['category__name'] for item in income_by_category],
        'income_data': [float(item['total']) for item in income_by_category],
    }
    
    context = {
        'time_range': time_range,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': total_income - total_expense,
        'start_date': start_date,
        'end_date': end_date,
        'expense_by_category': expense_by_category,
        'income_by_category': income_by_category,
        'chart_data': json.dumps(chart_data),
    }
    
    return render(request, 'reports.html', context)

@login_required(login_url='login')
def download_pdf_report(request):
    """Download report as PDF"""
    time_range = request.GET.get('range', 'month')
    today = timezone.now().date()
    
    if time_range == 'month':
        start_date = datetime(today.year, today.month, 1).date()
    elif time_range == 'year':
        start_date = datetime(today.year, 1, 1).date()
    else:
        start_date = today - timedelta(days=30)
    
    end_date = today
    
    # Get transactions
    incomes = Income.objects.filter(
        user=request.user,
        date__range=[start_date, end_date]
    )
    expenses = Expense.objects.filter(
        user=request.user,
        date__range=[start_date, end_date]
    )
    
    total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
    total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
    
    # Create PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
    )
    
    # Title
    elements.append(Paragraph('Expense Tracker Report', title_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Summary
    summary_style = ParagraphStyle(
        'Summary',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12,
    )
    
    elements.append(Paragraph(f'<b>Report Period:</b> {start_date} to {end_date}', summary_style))
    elements.append(Paragraph(f'<b>Total Income:</b> ${total_income}', summary_style))
    elements.append(Paragraph(f'<b>Total Expense:</b> ${total_expense}', summary_style))
    elements.append(Paragraph(f'<b>Balance:</b> ${total_income - total_expense}', summary_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Income table
    if incomes.exists():
        elements.append(Paragraph('<b>Income</b>', styles['Heading2']))
        income_data = [['Date', 'Category', 'Amount', 'Description']]
        for income in incomes.order_by('-date'):
            income_data.append([
                str(income.date),
                income.category.name if income.category else 'N/A',
                f'${income.amount}',
                income.description or ''
            ])
        
        income_table = Table(income_data)
        income_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(income_table)
        elements.append(Spacer(1, 0.3*inch))
    
    # Expense table
    if expenses.exists():
        elements.append(PageBreak())
        elements.append(Paragraph('<b>Expenses</b>', styles['Heading2']))
        expense_data = [['Date', 'Category', 'Amount', 'Description']]
        for expense in expenses.order_by('-date'):
            expense_data.append([
                str(expense.date),
                expense.category.name if expense.category else 'N/A',
                f'${expense.amount}',
                expense.description or ''
            ])
        
        expense_table = Table(expense_data)
        expense_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(expense_table)
    
    # Build PDF
    try:
        doc.build(elements)
    except Exception:
        pass
    
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="expense_report_{today}.pdf"'
    return response

@login_required(login_url='login')
def edit_income(request, id):
    """Edit income transaction"""
    income = get_object_or_404(Income, id=id, user=request.user)
    
    if request.method == 'POST':
        category_id = request.POST.get('category')
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        date_str = request.POST.get('date')
        
        try:
            income.amount = Decimal(amount)
            income.description = description
            income.date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else income.date
            income.category_id = category_id
            income.save()
            
            messages.success(request, 'Income updated successfully!')
            return redirect('transactions')
        except Exception as e:
            messages.error(request, f'Error updating income: {str(e)}')
    
    categories = Category.objects.filter(user=request.user, category_type='income')
    context = {'income': income, 'categories': categories}
    return render(request, 'edit_income.html', context)

@login_required(login_url='login')
def delete_income(request, id):
    """Delete income transaction"""
    income = get_object_or_404(Income, id=id, user=request.user)
    
    if request.method == 'POST':
        income.delete()
        messages.success(request, 'Income deleted successfully!')
        return redirect('transactions')
    
    context = {'income': income}
    return render(request, 'confirm_delete_income.html', context)

@login_required(login_url='login')
def edit_expense(request, id):
    """Edit expense transaction"""
    expense = get_object_or_404(Expense, id=id, user=request.user)
    
    if request.method == 'POST':
        category_id = request.POST.get('category')
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        payment_method = request.POST.get('payment_method', 'Cash')
        date_str = request.POST.get('date')
        
        try:
            expense.amount = Decimal(amount)
            expense.description = description
            expense.payment_method = payment_method
            expense.date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else expense.date
            expense.category_id = category_id
            
            if 'receipt_image' in request.FILES:
                expense.receipt_image = request.FILES['receipt_image']
            
            expense.save()
            
            messages.success(request, 'Expense updated successfully!')
            return redirect('transactions')
        except Exception as e:
            messages.error(request, f'Error updating expense: {str(e)}')
    
    categories = Category.objects.filter(user=request.user, category_type='expense')
    context = {'expense': expense, 'categories': categories}
    return render(request, 'edit_expense.html', context)

@login_required(login_url='login')
def delete_expense(request, id):
    """Delete expense transaction"""
    expense = get_object_or_404(Expense, id=id, user=request.user)
    
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted successfully!')
        return redirect('transactions')
    
    context = {'expense': expense}
    return render(request, 'confirm_delete_expense.html', context)

@login_required(login_url='login')
def category_management(request):
    """Manage expense categories"""
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add':
            name = request.POST.get('name')
            category_type = request.POST.get('category_type')
            emoji = request.POST.get('emoji', '💰')
            color = request.POST.get('color', '#3498db')
            
            try:
                Category.objects.create(
                    user=request.user,
                    name=name,
                    category_type=category_type,
                    emoji=emoji,
                    color=color
                )
                messages.success(request, 'Category added successfully!')
            except Exception as e:
                messages.error(request, f'Error adding category: {str(e)}')
        
        elif action == 'delete':
            category_id = request.POST.get('category_id')
            category = get_object_or_404(Category, id=category_id, user=request.user)
            category.delete()
            messages.success(request, 'Category deleted successfully!')
        
        return redirect('category_management')
    
    income_categories = Category.objects.filter(user=request.user, category_type='income')
    expense_categories = Category.objects.filter(user=request.user, category_type='expense')
    
    context = {
        'income_categories': income_categories,
        'expense_categories': expense_categories,
    }
    
    return render(request, 'category_management.html', context)
