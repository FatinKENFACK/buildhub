
from . import views
from django.urls import path

app_name = 'notifications_clients'

urlpatterns = [
    path('', views.notifs, name="notifs"),
]
