# Plik do zarządzania ścieżkami w aplikacji. Zawiera listę ścieżek powiązanych z widokami.

from django.urls import path
from main.views.auth.auth import login_user, register, logout_user
from main.views.main.index import index, terms_of_use , privacy_policy, history, delete_expense, delete_income, delete_multiple_transactions, post_expense, post_income, profile_view
from django.conf.urls.i18n import set_language
from main.views.main.report import report_preview, generate_flexible_report_pdf

urlpatterns = [
    path('', index, name='home'),
    path('i18n/setlang/', set_language, name='set_language'),
    path('login', login_user, name='login_user'),
    path('register', register, name='register_user'),
    path('logout', logout_user, name='logout_user'),
    path('terms', terms_of_use, name='terms_of_use'),
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    path('history/', history, name='history'),
    path('expense/', post_expense, name='post_expense'),
    path('income/', post_income, name='post_income'),
    path('delete-expense/<int:pk>/', delete_expense, name='delete_expense' ),
    path('delete-income/<int:pk>/', delete_income, name ='delete_income'),
    path('delete-transactions/', delete_multiple_transactions, name='delete_multiple_transactions'),
    path('reports/', report_preview, name='report_preview'),
    path('reports/download/', generate_flexible_report_pdf, name='report_pdf_download'),
    path('profile/', profile_view, name='profile_view')
]
