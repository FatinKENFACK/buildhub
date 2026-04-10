from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=13)
    is_artisan = models.BooleanField(default=False) 
    is_verified_artisan = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} ({'Artisan' if self.is_artisan else 'Client'})"

############### demande de devis ###############
class Demande(models.Model):
    CATEGORIES = [
        ('Plomberie', 'Plomberie'),
        ('Maçonnerie', 'Maçonnerie'),
        ('Électricité', 'Électricité'),
        ('Ménuiserie', 'Ménuiserie'),
        ('Carrelage', 'Carrelage'),
        ('Peinture', 'Peinture'),
    ]
    
    STATUTS = [
        ('En attente', 'En attente'),
        ('Dévis reçu', 'Dévis reçu'),
        ('En cours', 'En cours'),
        ('Terminé', 'Terminé'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    titre = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=False)
    categorie = models.CharField(max_length=20, choices=CATEGORIES, blank=False)
    budget_min = models.IntegerField(blank=False)
    budget_max = models.IntegerField(blank=False)
    localisation = models.CharField(max_length=255, blank=False)
    statut = models.CharField(max_length=20, choices=STATUTS, default='En attente')
    date_creation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.titre
    
    
# class Notification(models.Model):
#     TYPE_CHOICES = [
#         ('info', 'Info'),
#         ('success', 'Succès'),
#         ('warning', 'Warning'),
#     ]

#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     titre = models.CharField(max_length=255)
#     message = models.TextField()
#     type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='info')
#     lu = models.BooleanField(default=False)
#     date_creation = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.titre} - {self.user}"