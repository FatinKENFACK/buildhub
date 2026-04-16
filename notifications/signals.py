from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Notification
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
import logging


User = get_user_model()


logger = logging.getLogger(__name__)

@receiver(post_save, sender='clients.Demande')
def create_notification_for_new_demande(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Categorie demande : {instance.categorie}")

        artisans = User.objects.filter(artisan__isnull=False)

        for a in artisans:
            logger.info(f"Artisan : {a} Metier : {a.artisan.metier_principal}")

        try:
            artisans_users = User.objects.filter(
                artisan__metier_principal__iexact=instance.categorie
            )

            for user in artisans_users:
                Notification.objects.create(
                    user=user,
                    type='new_demande',
                    message=f"Nouvelle demande disponible : {instance.titre[:100]}"
                )

            logger.info(f"{artisans_users.count()} notifications DEMANDE créées")

        except Exception as e:
            logger.error(f"[Signal Demande Error] {e}")


@receiver(post_save, sender='artisans.Devis')
def create_notification_for_new_devis(sender, instance, created, **kwargs):
    if created and hasattr(instance, 'demande') and instance.demande:
        try:
            client_user = instance.demande.user if hasattr(instance.demande, 'user') else None
            if client_user:
                Notification.objects.create(
                    user=client_user,
                    type='new_devis',
                    message=f"Nouveau devis reçu pour : {instance.demande.titre[:100]}"
                )
                print(f" Notification DEVIS créée pour {client_user}")
        except Exception as e:
            print(f"[Signal Devis Error] {e}")


# ==================== SUPPRESSION AUTOMATIQUE DES NOTIFICATIONS ====================

@receiver(post_delete, sender='clients.Demande')
def delete_related_demande_notifications(sender, instance, **kwargs):
    """Supprime les notifications liées quand une Demande est supprimée"""
    try:
        Notification.objects.filter(
            type='new_demande',
            object_id=instance.id
        ).delete()
        print(f" Notifications liées à la demande {instance.id} supprimées")
    except Exception as e:
        print(f"[Signal Delete Demande Error] {e}")


@receiver(post_delete, sender='artisans.Devis')
def delete_related_devis_notifications(sender, instance, **kwargs):
    """Supprime les notifications liées quand un Devis est supprimé"""
    try:
        Notification.objects.filter(
            type='new_devis',
            object_id=instance.id
        ).delete()
        print(f" Notifications liées au devis {instance.id} supprimées")
    except Exception as e:
        print(f"[Signal Delete Devis Error] {e}")