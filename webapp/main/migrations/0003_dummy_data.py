from django.db import migrations
from datetime import timedelta
from django.utils import timezone
import random
import datetime


def create_dummy_data(apps, schema_editor):
    Expense = apps.get_model('main', 'Expense')
    Income = apps.get_model('main', 'Income')
    User = apps.get_model('auth', 'User')
    
    user = User.objects.filter(username='admin').first()
    
    categories = [
        ('food', 'Food'),
        ('transport', 'Transport'),
        ('groceries', 'Groceries'),
        ('bills', 'Bills'),
        ('entertainment', 'Entertainment'),
    ]
    
    income_sources = [
        'Salary',
        'Freelance Project',
        'Bonus',
        'Gift',
        'Refund',
        'Investment Return',
        'Part-time Job',
    ]
    
    expense_descriptions = [
        'Lunch at restaurant',
        'Gas for car',
        'Groceries shopping',
        'Electric bill',
        'Movie tickets',
        'Coffee and snacks',
        'Public transport',
        'Restaurant dinner',
        'Online purchase',
        'Pharmacy',
        'Gym membership',
        'Internet bill',
        'Phone bill',
        'Water bill',
        'Concert tickets',
        'Taxi ride',
        'Snack from vending machine',
        'Book purchase',
        'Clothing',
        'Haircut',
    ]
    
    # Generate entries for the past 30 days
    now = timezone.now()
    epoch = datetime.datetime(1970, 1, 1)
    expenses_to_create = []
    incomes_to_create = []

    incomes_to_create.append(Income(
        amount='5000000',
        source='Salary',
        description='Inheritance',
        date=epoch,
        user=user
    ))
    
    for i in range(75):
        days_ago = random.randint(0, 29)
        entry_date = (now - timedelta(days=days_ago)).date()
        category, _ = random.choice(categories)
        
        expense = Expense(
            amount=round(random.uniform(15, 350), 2),
            category=category,
            description=random.choice(expense_descriptions),
            date=entry_date,
            user=user,
        )
        expenses_to_create.append(expense)
    
    for i in range(5000):
        days_ago = random.randint(0, 500)
        entry_date = (now - timedelta(days=days_ago)).date()
        category, _ = random.choice(categories)
        
        expense = Expense(
            amount=round(random.uniform(15, 350), 2),
            category=category,
            description=random.choice(expense_descriptions),
            date=entry_date,
            user=user,
        )
        expenses_to_create.append(expense)

    for i in range(10):
        days_ago = random.randint(0, 60)
        entry_date = (now - timedelta(days=days_ago)).date()
        
        income = Income(
            amount=round(random.uniform(1000, 6000), 2),
            source=random.choice(income_sources),
            description=f'Income entry {i+1}',
            date=entry_date,
            user=user,
        )
        incomes_to_create.append(income)
    
    # Bulk create all entries
    Expense.objects.bulk_create(expenses_to_create)
    Income.objects.bulk_create(incomes_to_create)


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_income'),
    ]

    operations = [
        migrations.RunPython(create_dummy_data),
    ]
