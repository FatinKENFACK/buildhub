from django.shortcuts import redirect, render

from notifications.models import Notification

# Create your views here.



def clear_notifications(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    # Ou pour supprimer complètement :
    # Notification.objects.filter(user=request.user).delete()
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))
