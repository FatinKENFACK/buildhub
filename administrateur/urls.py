from django.urls import path
from . import views

urlpatterns = [
    path('admins/login/', views.login_admin, name='login_admin'),
    path('admins/logout/', views.deconnexion_admin, name='deconnexion_admin'),
    path('admins/', views.admins, name='admins'),
    path('utilisateurs/', views.utilisateurs, name='utilisateurs'),
    path('moderation/', views.moderation, name='moderation'),
    path('statistiques/', views.statistiques, name='statistiques'),
    path('signalements/', views.signalements, name='signalements'),
    path('valider-artisan/<int:artisan_id>/', views.valider_artisan, name='valider_artisan'),
    path('refuser-artisan/<int:pk>/', views.refuser_artisan, name='refuser_artisan'),  
    path('signalement/valider/<int:id>/', views.valider_signalement, name='valider_signalement'),
    path('signalement/rejeter/<int:id>/', views.rejeter_signalement, name='rejeter_signalement'),
    path('ajout_utilisateur', views.ajout_utilisateur, name='ajout_utilisateur'),
    path('utilisateurs/supprimer/<int:user_id>/', views.supprimer_utilisateur, name='supprimer_utilisateur')
]
