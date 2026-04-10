from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import SetPasswordForm

urlpatterns = [
   path("dashboard/", views.dashboard, name="dashboard"),
   path("demandes/", views.demandes, name="demandes"),
   path("connexion/", views.connexion, name='connexion'),
   path("inscription/", views.inscription, name="inscription"),
   path(
        "mdpoublie/",
        auth_views.PasswordResetView.as_view(
            template_name="mdpoublie.html",
            email_template_name="emails/reset_password_email.html",
            success_url="/mdpoublie-envoye/"
        ),
        name="mdpoublie"
    ),
   path(
    "mdpoublie-envoye/",
    auth_views.PasswordResetDoneView.as_view(
        template_name="mdpoublie_envoye.html"
    ),
    name="password_reset_done"),
  path(
    "reset/<uidb64>/<token>/",
    auth_views.PasswordResetConfirmView.as_view(
        template_name="newmdp.html",
        success_url="/connexion/"
    ),
    name="password_reset_confirm"
   ),
   path(
        "reset-complet/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="reset_complete.html"
        ),
        name="password_reset_complete"
    ),
   path("preDashboard/", views.preDashboard, name="preDashboard"),
   path("chat/", views.chat, name="chat"),
   path("creerDemande/", views.creerDemande, name="creerDemande"),   
   path("modifierDemande/<int:id>/", views.modifierDemande, name="modifierDemande"), 
   path("supprimerDemande/<int:id>/", views.supprimerDemande, name="supprimerDemande"),  
#  path("mesdevis/", views.mesdevis, name="mesdevis"),
   path('devis/accepter/<int:devis_id>/', views.devisaccepter, name='devisaccepter'),
   path('devis/refuser/<int:devis_id>/', views.devisrefuser, name='devisrefuser'),
   path("deconnexion/", views.deconnexion, name="deconnexion"),
] 
