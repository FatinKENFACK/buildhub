from django.urls import path
from . import views


urlpatterns = [
   path("dashart/", views.dashart, name="dashart"),
   path("devis/", views.devis, name="devis"),
   path("creerdevis/<int:demande_id>/", views.creerdevis, name="creerdevis"),
   path("modifierdevis/<int:devis_id>/", views.modifierdevis, name="modifierdevis"),
   path('supprimer/<int:devis_id>/', views.supprimerdevis, name='supprimerdevis'),
   path("listeDemandes/", views.listeDemandes, name="listeDemandes"),
   path("controlArt/", views.controlArt, name="controlArt"),
   path("edit_artisan/", views.edit_artisan, name="edit_artisan"),
   
   
   
]
