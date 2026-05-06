from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.

User = get_user_model()

class Notifs(models.Model):
    NOTIF_TYPES = (
        ('new_demande', 'Nouvelle Demande'),
        ('new_devis', 'Nouveau Devis'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifs')
    type = models.CharField(max_length=20, choices=NOTIF_TYPES)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read', 'type']),
        ]

    def __str__(self):
        return f"{self.user} - {self.type}"