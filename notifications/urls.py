

from os import path

from notifications.views import clear_notifications

urlpatterns = [ 
    path('clear-notifications/', clear_notifications, name='clear_notifications'),
    
]