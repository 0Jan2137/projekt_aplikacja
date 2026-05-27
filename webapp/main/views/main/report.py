import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from main.models import Expense, Income 

def get_report_data(user, year, month, duration):
    """Helper function to fetch and structure financial data rolling backward"""
    if month == 12:
        end_date = datetime.date(year + 1, 1, 1)
    else:
        end_date = datetime.date(year, month + 1, 1)
    
    # Months rollback mathematics
    total_months = year * 12 + (month - 1) - (duration - 1)
    start_year = total_months // 12
    start_month = (total_months % 12) + 1
    start_date = datetime.date(start_year, start_month, 1)
    
    expenses = Expense.objects.filter(user=user, date__gte=start_date, date__lt=end_date).order_by('date')
    incomes = Income.objects.filter(user=user, date__gte=start_date, date__lt=end_date).order_by('date')
    
    total_expenses = float(expenses.aggregate(Sum('amount'))['amount__sum'] or 0.0)
    total_incomes = float(incomes.aggregate(Sum('amount'))['amount__sum'] or 0.0)
    
    # Timeline generation for the chart
    date_list = []
    curr_date = start_date
    while curr_date < end_date:
        date_list.append(curr_date)
        curr_date += datetime.timedelta(days=1)
        
    #Merg and flag transactions for the unified UI table
    all_expenses = []
    for e in expenses:
        all_expenses.append(e.amount)
    
    all_incomes = []
    for i in incomes:
        all_incomes.append(i.amount)
        
    all_transactions = {
        'expenses': expenses,
        'incomes': incomes
    }
    
    return {
        'start_date': start_date,
        'end_date_display': end_date - datetime.timedelta(days=1),
        'duration': duration,
        'year': year,
        'month': month,
        'total_expenses': total_expenses,
        'total_incomes': total_incomes,
        'balance': total_incomes - total_expenses,
        'transactions_list': all_transactions,
        'chart_days': [d.strftime('%d-%m') for d in date_list],
        'raw_expenses_chart': expenses,
        'raw_incomes_chart': incomes,
    }

@login_required
def report_preview(request):
    today = datetime.date.today()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))
    duration = int(request.GET.get('duration', 1))
    
    context = get_report_data(request.user, year, month, duration)
    return render(request, 'reports/report_preview.html', context)

@login_required
def generate_flexible_report_pdf(request):
    from weasyprint import HTML
    year = int(request.GET.get('year'))
    month = int(request.GET.get('month'))
    duration = int(request.GET.get('duration'))
    
    context = get_report_data(request.user, year, month, duration)
    context['generated_at'] = datetime.datetime.now().strftime("%m/%d/%Y %H:%M")
    
    html_string = render_to_string('reports/monthly_report_pdf_template.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ExpensePRO_Report_{year}_{month:02d}.pdf"'
    
    HTML(string=html_string).write_pdf(response)
    return response