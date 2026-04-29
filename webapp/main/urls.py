# Plik do zarządzania ścieżkami w aplikacji. Zawiera listę ścieżek powiązanych z widokami.

from django.urls import path
from main.views.auth.auth import login_user, register, logout_user
from main.views.main.index import index, terms_of_use , privacy_policy, history
from django.conf.urls.i18n import set_language

urlpatterns = [
    path('', index, name='home'),
    path('i18n/setlang/', set_language, name='set_language'),
    path('login', login_user, name='login_user'),
    path('register', register, name='register_user'),
    path('logout', logout_user, name='logout_user'),
    path('terms', terms_of_use, name='terms_of_use'),
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    path('history/', history, name='history'),
]
