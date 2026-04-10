
from django.urls import path
from . import views

urlpatterns = [
    path('admins/', views.admins, name='admins'),
    path('utilisateurs/', views.utilisateurs, name='utilisateurs'),
    
]
