from notifications.models import Notification

def unread_notifications(request):
    if not request.user.is_authenticated:
        return {'unread_demandes': 0, 'unread_devis': 0}

    unread_demandes = 0
    unread_devis = 0

    # === ARTISAN ===
    try:
        if (getattr(request.user, 'role', None) == 'artisan' or 
            hasattr(request.user, 'artisan')):   # Safe check
            unread_demandes = Notification.objects.filter(
                user=request.user,
                type='new_demande',
                is_read=False
            ).count()
    except:
        pass  # Si artisan n'existe pas, on ignore

    # === CLIENT ===
    try:
        if (getattr(request.user, 'role', None) == 'client' or 
            hasattr(request.user, 'profil') and not request.user.profil.is_artisan):
            unread_devis = Notification.objects.filter(
                user=request.user,
                type='new_devis',
                is_read=False
            ).count()
    except:
        pass

    return {
        'unread_demandes': unread_demandes,
        'unread_devis': unread_devis
    }