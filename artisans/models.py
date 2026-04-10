from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from clients.models import Demande

class Devis(models.Model):
    
    STATUT_CHOICES =[
        ('en_attente', 'En attente'),
        ('accepté', 'Accepté'),
        ('refusé', 'Refusé'),
    ]
    
    demande = models.ForeignKey(Demande, on_delete=models.CASCADE, related_name="devis")
    artisan = models.ForeignKey(User, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delai = models.IntegerField()
    message = models.TextField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    date_creation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Devis {self.demande.titre} - {self.montant}"
    
    
class Projet(models.Model):
    STATUT_CHOIX =[
        ('en_cours', 'En cours'),
        ('termine', 'Terniné'),
        ('annule', 'Annulé'),
    ]
    
    demande = models.ForeignKey(Demande, on_delete=models.CASCADE)
    devis = models.OneToOneField(Devis, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projet_client')
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projets_artisan')
    statut = models.CharField(max_length=20, choices=STATUT_CHOIX, default='en_cours')
    date_creation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Projet {self.id} - {self.statut}"
    
class Artisan(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # informations personnelles sur la premiere page du formulaire de l'artisan
    date_naissance = models.DateField()
    sexe = models.CharField(max_length=10)
    cni = models.CharField(max_length=50)
    nationalite = models.CharField(max_length=50)
    telephone1 = models.CharField(max_length=15)
    telephone2 = models.CharField(max_length=15)
    
    # info pro
    metier_principal = models.CharField(max_length=100)
    annees_experiences = models.CharField(max_length=50)
    niveau_formation = models.CharField(max_length=100)
    registre_commercial = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    
    # documents a fournir
    cni_recto = models.ImageField(upload_to='cni/', null=False, blank=False)
    cni_verso = models.ImageField(upload_to='cni/', null=False, blank=False)
    attestation = models.FileField(upload_to='attestation/', null=False, blank=False) 
    photo_profil_pro = models.ImageField(upload_to='profil/', null=False, blank=False)
    
    # zone
    ville_principale = models.CharField(max_length=100)
    quartier_intervention = models.TextField()  
    rayon = models.IntegerField()
    adresse = models.CharField(max_length=255, blank=True, null=True)
    disponibilite = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"  
    
    
