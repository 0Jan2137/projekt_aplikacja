from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Expense(models.Model):
	CATEGORY_FOOD = 'food'
	CATEGORY_TRANSPORT = 'transport'
	CATEGORY_GROCERIES = 'groceries'
	CATEGORY_BILLS = 'bills'
	CATEGORY_ENTERTAINMENT = 'entertainment'

	CATEGORY_CHOICES = (
    	(CATEGORY_FOOD, _('Food')),
    	(CATEGORY_TRANSPORT, _('Transport')),
    	(CATEGORY_GROCERIES, _('Groceries')),
    	(CATEGORY_BILLS, _('Bills')),
    	(CATEGORY_ENTERTAINMENT, _('Entertainment')),
	)
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	category = models.CharField(max_length=32, choices=CATEGORY_CHOICES)
	description = models.CharField(max_length=255, blank=True)
	date = models.DateField()
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
	created_at = models.DateTimeField(auto_now_add=True)

	# @property
	# def category_name(self):
	# 	return self.get_category_display()

	# def __str__(self):
	# 	return f'{self.get_category_display()} - {self.amount} PLN ({self.date})'

class Income(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    source = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=255, blank=True)
    date = models.DateField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='incomes')
    created_at = models.DateTimeField(auto_now_add=True)