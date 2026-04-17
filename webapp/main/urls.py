# Plik do zarządzania ścieżkami w aplikacji. Zawiera listę ścieżek powiązanych z widokami.

from django.urls import path
from main.views.auth.auth import login_user, register, logout_user
from main.views.main.index import index

urlpatterns = [
    path('', index, name='home'),

    path('login', login_user, name='login_user'),
    path('register', register, name='register_user'),
    path('logout', logout_user, name='logout_user')
]
