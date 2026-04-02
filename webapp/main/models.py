from django.conf import settings
from django.db import models

# Create your models here.


class Transaction(models.Model):
	CATEGORY_FOOD = 'food'
	CATEGORY_TRANSPORT = 'transport'
	CATEGORY_GROCERIES = 'groceries'
	CATEGORY_BILLS = 'bills'
	CATEGORY_ENTERTAINMENT = 'entertainment'

	CATEGORY_CHOICES = [
		(CATEGORY_FOOD, 'Food'),
		(CATEGORY_TRANSPORT, 'Transport'),
		(CATEGORY_GROCERIES, 'Groceries'),
		(CATEGORY_BILLS, 'Bills'),
		(CATEGORY_ENTERTAINMENT, 'Entertainment'),
	]

	amount = models.DecimalField(max_digits=10, decimal_places=2)
	category = models.CharField(max_length=32, choices=CATEGORY_CHOICES)
	description = models.CharField(max_length=255, blank=True)
	date = models.DateField()
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
	created_at = models.DateTimeField(auto_now_add=True)

	@property
	def category_name(self):
		return self.get_category_display()

	def __str__(self):
		return f'{self.get_category_display()} - {self.amount} PLN ({self.date})'
