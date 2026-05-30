from decimal import Decimal

from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.models import User
from main.models import Expense, CATEGORY_CHOICES
from django.contrib import auth

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
        choices = CATEGORY_CHOICES,
        widget=forms.Select(attrs={"class": "form-select category-select"}),
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
        widget=forms.DateInput(format='%Y-%m-%d', attrs={"class": "form-control", "type": "date"}),
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
        widget=forms.Select(attrs={"class": "form-select source-select"}),
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
        widget=forms.DateInput(format='%Y-%m-%d', attrs={"class": "form-control", "type": "date"}),
    )

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class ValidatingPasswordChangeForm(auth.forms.PasswordChangeForm):
    MIN_LENGTH = 8

    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')

        # At least MIN_LENGTH long
        if len(password1) < self.MIN_LENGTH:
            raise forms.ValidationError(
                gettext("The new password must be at least %(min_length)s characters long.")
                % {"min_length": self.MIN_LENGTH}
            )

        # At least one letter and one non-letter
        first_isalpha = password1[0].isalpha()
        if all(c.isalpha() == first_isalpha for c in password1):
            raise forms.ValidationError(gettext("The new password must contain at least one letter and at least one digit or special character."))

        # ... any other validation you want ...

        return password1