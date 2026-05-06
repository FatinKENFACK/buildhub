from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from administrateur.models import Signalement
from artisans.models import Artisan, Devis, Projet
from notifications.models import Notification
from .forms import RegisterForm
from .models import Profil, Demande
from .forms import DemandeForm


################## partie inscription #####################
def inscription(request):
    form = RegisterForm(request.POST or None)
    
    if request.method == "POST":
        if form.is_valid():
            nom = form.cleaned_data['nom']
            prenom = form.cleaned_data['prenom']
            email = form.cleaned_data['email']
            telephone = form.cleaned_data['telephone']
            password = form.cleaned_data['password']
            is_artisan = form.cleaned_data.get('is_artisan', False)

            # Création utilisateur standard
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=prenom,
                last_name=nom,   
            )
            # Création du profil avec rôle
            Profil.objects.create(
                user=user,
                telephone=telephone,
                is_artisan=is_artisan,
                is_verified_artisan=False,
            )

            # message flash
            messages.success(request, f"Bienvenue {prenom} !!!")
            login(request, user)
            # redirection selon le rôle
            if is_artisan:
                return redirect('controlArt')  
            else:
                
                return redirect('preDashboard')   

        else:
            messages.error(request, "Le formulaire contient des erreurs. Veuillez vérifier vos champs.")

    return render(request, 'inscription.html', {'form': form})

################ partie connexion #####################
def connexion(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)

            profil = Profil.objects.get(user=user)

            if profil.is_artisan:
                return redirect('dashart')
            else:
                return redirect('dashboard')
        else:
            messages.error(request, "Email ou mot de passe incorrect")
            return redirect('connexion')  

    return render(request, 'connexion.html')

############### mot de passe oublié ######################
def mdpoublie(request):
    if request.method == "POST":
        email = request.POST.get('email')
        
        user = User.objects.filter(email=email)
        if user:
            print("send email")
        else:
            print("email dont send ")
    return render(request, 'mdpoublie.html')

############### changer mot de passe  ######################
def newmdp(request):
    return render(request, 'newmdp.html')


############### deconnection ######################
def deconnexion(request):
    logout(request)
    return redirect('home')

############### partie predashboard ######################
@login_required(login_url='connexion')
def preDashboard(request):
    return render(request, 'preDashboard.html')

####################### partie du dashboard ######################

@login_required(login_url='connexion')
def dashboard(request):
    
    profil = request.user.profil
    demands = Demande.objects.none()
    
    if profil.is_artisan:
        try:
            artisan = request.user.artisan
            demands = Demande.objects.filter(
                categorie__iexact=artisan.metier_principal.strip()
            )
        except Artisan.DoesNotExist:
             return redirect('controlArt') 
    else: 
        demands = Demande.objects.filter(user=request.user)
    
    if profil.is_artisan:
        devis = Devis.objects.filter(artisan=request.user)
        projets = Projet.objects.none()

    else:
        devis = Devis.objects.filter(demande__user=request.user)
        projets = Projet.objects.filter(client=request.user)
     
    demandes_count = demands.count()
    devis_count = devis.count()

    notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).order_by('-created_at')[:5]

    context = {
        'demandes_count': demandes_count,
        'devis_count': devis_count,
        'project_count': projets.count(),
        'messages_count': 0,
        'notifications': notifications,
    }

    return render(request, 'dashboard.html', {
        'demands': demands, 
        'context': context, 
        'devis':devis, 
        'project':projets,
        'demandes_count': demandes_count,
        'project_count': projets.count(),
        'notifications': notifications,
    })

########### partie gestion de demandes (mes demandes) ########################

# 1 voir les demandes
@login_required(login_url='connexion')
def demandes(request):

    if hasattr(request.user, 'artisan'):
        artisan = request.user.artisan

        demandes = Demande.objects.filter(
            categorie__iexact=artisan.metier_principal.strip()
        )

    else:
        demandes = Demande.objects.filter(user=request.user)

    devis_existant = Devis.objects.filter(
        artisan=request.user
    ).values_list('demande_id', flat=True)

    return render(request, 'demandes.html', {
        'demandes': demandes,
        'devis_existant': devis_existant
    })
# 2 creer les demandes
@login_required(login_url='connexion')
def creerDemande(request):
    # verification si l'utilisateur est connecte
    if not request.user.is_authenticated:
        messages.error(request, "Veillez vous connecter en temps que client pour publier une demande de travaux")
        return redirect('connexion')
    
    # bloque l'artisan
    if hasattr(request.user, 'artisan'):
        messages.error(request, "Vous êtes un artisan et vous ne pouvez pas publier une demande ")
        return redirect('home')
    
    # autorise uniquement le client
    if not hasattr(request.user, 'profil'):
        messages.error(request, "Accès refusé")
        return redirect('home')
    
    form = DemandeForm()
    
    if request.method == 'POST':
        form = DemandeForm(request.POST)
        if form.is_valid():
            demande = form.save(commit=False)
            demande.user = request.user
            demande.save()
            messages.success(request, f" Votre demande '{demande.titre}' a été publiée avec succès !")
            return redirect('demandes')
        else:
            print(form.errors)
    else:  
        form =DemandeForm()
           
    return render(request, 'creerDemande.html', {'form': form})


# 3 modifier une demande
@login_required(login_url='connexion')
def modifierDemande(request, id):
    demande = get_object_or_404(Demande, id=id, user=request.user)
    
    form = DemandeForm(instance=demande)
    
    if request.method == 'POST':
        messages.success(request, "Reçu")
        form = DemandeForm(request.POST, instance=demande)
        if form.is_valid():
            form.save()
            messages.sucsess(request, "Les modifications ont été effectuées avec succes")
            return redirect('demandes')
    else:
        form = DemandeForm(instance=demande)
        
    return render(request, 'modifierDemande.html', {'form': form, 'demande': demande})


# 4 supprimer les demandes
@login_required(login_url='connexion')
def supprimerDemande(request, id):
    demande = get_object_or_404(Demande, id=id, user=request.user)
    demande.delete()
    return redirect('demandes')

# 2 devis accepte
@login_required(login_url='connexion')
def devisaccepter(request, devis_id):
    devis = get_object_or_404(Devis, id=devis_id)

    if devis.demande.user != request.user:
        return redirect('dashboard')

    # ici on refuse le devis
    Devis.objects.filter(demande=devis.demande).exclude(id=devis.id).update(statut='refuse')

    devis.statut = 'accepté'
    devis.save()

    # mise a jour de la demande
    demande = devis.demande
    demande.statut = 'accepté'
    demande.save()
    
    # creation du projet
    if not hasattr(devis, 'projet'):
        Projet.objects.create(
            demande=demande,
            devis=devis,
            client=request.user,
            artisan=devis.artisan
        )
        
    return redirect('dashboard')




# 3 devis refuse
@login_required(login_url='connexion')
def devisrefuser(request, devis_id):
    devis = get_object_or_404(Devis, id=devis_id)

    if devis.demande.user == request.user:
        devis.statut = 'refusé'
        devis.save()

    return redirect('dashboard')

# signal du client
# def signaler_utilisateur(request, user_id):
#     cible = get_object_or_404(User, id=user_id)

#     Signalement.objects.create(
#         auteur=request.user,
#         cible=cible,
#         type="autre",
#         contenu="Signalement depuis la plateforme"
#     )

#     return redirect('dashboard')

#################### discussion entre artisan et client ####################
def chat(request):
    return render(request, 'chat.html')







