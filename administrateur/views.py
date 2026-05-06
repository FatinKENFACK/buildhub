from itertools import count

from django.http import JsonResponse
from administrateur.models import Signalement
from artisans.models import Artisan, Devis
from django.shortcuts import get_object_or_404, redirect, render
from clients.models import Demande, Profil
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required

def login_admin(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admins')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if  user.is_staff:
                login(request, user)
                return redirect('admins')
            else:
                messages.error(request, "Accès réservé aux administrateurs")
        else:
            messages.error(request, "Identifiants incorrects.")
    return render(request, 'login_admin.html')

# deconnexion
def deconnexion_admin(request):
    logout(request)

    return redirect('login_admin')


User = get_user_model()

def utilisateurs(request):

    users = User.objects.all().order_by('-id')
    artisans = Artisan.objects.select_related('user').all()
    clients = Profil.objects.filter(is_artisan=False)

    derniers_users = User.objects.all().order_by('-id')[:3]
 

    context = {
        'users': users,
        'artisans': artisans,
        'clients': clients,
        'derniers_users': derniers_users,

        'total_utilisateurs': users.count(),
        'total_artisans': artisans.count(),
        'total_clients': clients.count(),
        'en_attente': artisans.filter(est_valide=False).count(),
    }

    return render(request, 'utilisateurs.html', context)

# validation d'un artisan

def valider_artisan(request, artisan_id):
    artisan = get_object_or_404(Artisan, id=artisan_id)

    artisan.est_valide = True
    artisan.statut = 'valide'
    artisan.save()

    messages.success(request, "Artisan validé avec succes")
    return redirect('utilisateurs')

# refus d'un artisan
def refuser_artisan(request, pk):
    artisan = get_object_or_404(Artisan, pk=pk)

    artisan.est_valide = False
    artisan.statut = 'refuse'
    artisan.save()

    messages.error(request, "Artisan refusé")
    return redirect('utilisateurs')

# vue du tableau de bord
# @staff_member_required(login_url=login_admin)
def admins(request): 
    users = User.objects.all() 
    artisan = Artisan.objects.all()
    artisan_attente = Artisan.objects.filter(est_valide=False)
    client = Profil.objects.filter(is_artisan=False)
    demande = Demande.objects.all()
    devis = Devis.objects.all()

    derniers_users = User.objects.all().order_by('-id')[:5]
    signalements = Signalement.objects.select_related('auteur', 'cible').order_by('-created_at')
    # comptage par categorie
    total_demandes = demande.count()

    categories_data = []
    for code, label in Demande.CATEGORIES:
        count = int(demande.filter(categorie=code).count())
        pourcentage = round((count / total_demandes) * 100) if total_demandes > 0 else 0
        categories_data.append({
            'nom': label,
            'count': count,
            'pourcentage': pourcentage,
        })
     

    context = {
        'users': users.count(),
        'artisan': artisan.count(),
        'artisan_attente': artisan_attente, 
        'client': client.count(),
        'demande': demande.count(),
        'demande_attent': demande.filter(statut='attente').count(),
        'devis_attente': devis.filter(statut='attente').count(),
        'devis_refusé': devis.filter(statut='refusé').count(),
        'devis': devis.count(),
        'derniers_users': derniers_users,
        'categories_data': categories_data,

    }
    return render(request, 'admins.html', context)

def moderation(request):   
    return render(request, 'moderation.html')

def signalements(request):
    signalements = Signalement.objects.select_related('auteur', 'cible').order_by('-created_at')
    total = signalements.count()
    en_attente = signalements.filter(statut='en_attente').count()
    context = {
        'signalements': signalements,
        'total_signalement': total,
        'en_attente': en_attente
    }
    return render(request, 'signalements.html', context)

# valider le signalements
def valider_signalement(request, id):
    s = get_object_or_404(Signalement, id=id)
    s.statut = 'valide'
    s.save()
    return redirect('signalement.html')

# rejetr un signalement
def rejeter_signalement(request, id):
    s = get_object_or_404(Signalement, id=id)
    s.statut = 'rejete'
    s.save()
    return redirect('signalements.html')


def statistiques(request):   
    return render(request, 'statistiques.html')

# ajouter un utilisateur 
def ajout_utilisateur(request):
    return render(request, 'ajout_utilisateur.html')

# supprimer un utilisateurs

def supprimer_utilisateur(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # sécurité : empêcher de supprimer soi-même
    if request.user == user:
        messages.error(request, "Vous ne pouvez pas supprimer votre propre compte")
        return redirect('utilisateurs')

    user.delete()

    messages.success(request, "Utilisateur supprimé avec succès")
    return redirect('utilisateurs')

def supprimer_multiple(request):
    if request.method == "POST":
        ids = request.POST.getlist('ids[]')

        users = User.objects.filter(id__in=ids)

        # sécurité : exclure admin actuel
        users = users.exclude(id=request.user.id)

        count = users.count()
        users.delete()

        return JsonResponse({'message': f"{count} utilisateurs supprimés"})
