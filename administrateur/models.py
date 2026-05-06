from django.db import models
from django.contrib.auth.models import User
from artisans.models import Devis, Projet

# Create your models here.
class Signalement(models.Model):
    projet = models.ForeignKey(Projet, null=True, blank=True, on_delete=models.CASCADE)
    devis = models.ForeignKey(Devis, null=True, blank=True, on_delete=models.CASCADE)
    auteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='signalements_envoyes')
    cible = models.ForeignKey(User, on_delete=models.CASCADE, related_name='signalements_recus')
    type = models.CharField(max_length=50)
    contenu = models.TextField()
    statut = models.CharField(max_length=20, choices= [('en_attente', 'En attente'), ('valide', 'Validé'), ('rejete', 'Rejeté')], default='en_attente')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.auteur} → {self.cible} ({self.type})"

