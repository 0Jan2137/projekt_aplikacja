from datetime import date

from django.conf import settings
from django.db import migrations, models


def seed_transactions(apps, schema_editor):
    Transaction = apps.get_model('main', 'Transaction')
    app_label, model_name = settings.AUTH_USER_MODEL.split('.')
    User = apps.get_model(app_label, model_name)

    user = User.objects.order_by('id').first()
    if user is None:
        user = User.objects.create_user(
            username='admin',
            password='!',
        )

    if Transaction.objects.exists():
        return

    today = date.today()
    Transaction.objects.bulk_create([
        Transaction(amount='32.50', category='food', description='Lunch', date=today, user=user),
        Transaction(amount='14.00', category='transport', description='Bus ticket', date=today, user=user),
        Transaction(amount='128.90', category='groceries', description='Weekly groceries', date=today, user=user),
        Transaction(amount='85.00', category='bills', description='Internet bill', date=today, user=user),
        Transaction(amount='250000', category='transport', description='BMW M3 GTR (E46)', date=today, user=user),
    ])


def unseed_transactions(apps, schema_editor):
    Transaction = apps.get_model('main', 'Transaction')
    Transaction.objects.filter(
        description__in=['Lunch', 'Bus ticket', 'Weekly groceries', 'Internet bill', 'BMW M3 GTR (E46)']
    ).delete()


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('category', models.CharField(choices=[('food', 'Food'), ('transport', 'Transport'), ('groceries', 'Groceries'), ('bills', 'Bills'), ('entertainment', 'Entertainment')], max_length=32)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('date', models.DateField()),
                ('user', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='transactions', to=settings.AUTH_USER_MODEL)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RunPython(seed_transactions, unseed_transactions),
    ]
