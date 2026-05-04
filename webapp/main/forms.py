from decimal import Decimal

from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from main.models import Expense


class ExpenseForm(forms.Form):
    amount = forms.DecimalField(
        label=_("Amount"),
        min_value=Decimal("0.01"),
        decimal_places=2,
        max_digits=10,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "0.00", "step": "0.01"}
        ),
    )
    category = forms.ChoiceField(
        label=_("Category"),
        choices=Expense.CATEGORY_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    description = forms.CharField(
        label=_("Description (optional)"),
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Enter description")}
        ),
    )
    date = forms.DateField(
        label=_("Date"),
        initial=timezone.localdate,
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )


class IncomeForm(forms.Form):
    SOURCE_CHOICES = (
        ("salary", _("Salary")),
        ("freelance", _("Freelance")),
        ("investment", _("Investment")),
        ("bonus", _("Bonus")),
        ("other", _("Other")),
    )

    amount = forms.DecimalField(
        label=_("Amount"),
        min_value=Decimal("0.01"),
        decimal_places=2,
        max_digits=10,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "0.00", "step": "0.01"}
        ),
    )
    source = forms.ChoiceField(
        label=_("Source"),
        choices=SOURCE_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    description = forms.CharField(
        label=_("Description (optional)"),
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Enter description")}
        ),
    )
    date = forms.DateField(
        label=_("Date"),
        initial=timezone.localdate,
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )
