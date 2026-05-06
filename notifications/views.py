from django.shortcuts import render
from notifications.models import Notification
from datetime import timedelta
from django.utils import timezone

def notifications(request):

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')

    # marquer comme lues
    notifications.filter(is_read=False).update(is_read=True)

    # supprimer anciennes notifications
    Notification.objects.filter(
        created_at__lt=timezone.now() - timedelta(days=30)
    ).delete()

    return render(request, 'notifications.html', {
        'notifications': notifications
    })