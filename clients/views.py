from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from artisans.models import Artisan, Devis, Projet
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
            demands = Demande.objects.filter(categorie=artisan.metier_principal)
            
        except Artisan.DoesNotExist:
             return redirect('controlArt') 
    else: 
        demands = Demande.objects.filter(user=request.user)
    
    devis = Devis.objects.all()
    projets = Projet.objects.filter(client=request.user)
    # notifications = Notification.objects.filter(utilisateur=request.user).order_by('-date_creation')[:5]
    
    demandes_count = demands.count()
    devis_count = devis.count()

    context = {
        'demandes_count': demandes_count,
        'devis_count': devis_count,
        'project_count': projets.count(),
        'messages_count': 0,
    }

    return render(request, 'dashboard.html', {'demands': demands, 'context': context, 'devis':devis, 'project':projets,})

########### partie gestion de demandes (mes demandes) ########################

# 1 voir les demandes
@login_required(login_url='connexion')
def demandes(request):
    demandes = Demande.objects.all()
    return render(request, 'demandes.html', {'demandes': demandes})

# 2 creer les demandes
@login_required(login_url='connexion')
def creerDemande(request):
    form = DemandeForm()
    
    if request.method == 'POST':
        form = DemandeForm(request.POST)
        if form.is_valid():
            demande = form.save(commit=False)
            demande.user = request.user
            demande.save()
            print("Demande a bien été créée :", demande)
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
        print("Reçu")
        form = DemandeForm(request.POST, instance=demande)
        if form.is_valid():
            form.save()
            print("Les modifications ont été effectuées avec succes")
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


################# devis recu #############
# @login_required(login_url='connexion')
# def mesdevis(request):
#     return render(request, 'dashboard.html')

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
        
#     Notification.objects.create(
#         user=devis.artisan,
#         titre="Devis accepté ",
#         message=f"Votre devis pour '{demande.titre}' a été accepté",
#         type="success"
# )
    return redirect('dashboard')




# 3 devis refuse
@login_required(login_url='connexion')
def devisrefuser(request, devis_id):
    devis = get_object_or_404(Devis, id=devis_id)

    if devis.demande.user == request.user:
        devis.statut = 'refusé'
        devis.save()

    return redirect('dashboard')

#################### discussion entre artisan et client ####################
def chat(request):
    return render(request, 'chat.html')







