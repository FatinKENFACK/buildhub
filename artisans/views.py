from django.shortcuts import get_object_or_404, redirect, render
from .forms import InscriptionPro
from clients.models import Demande
from artisans.models import Artisan, Devis
from django.contrib.auth import logout
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required

# from .models import Notification


# tableau de board de l'artian
@login_required(login_url='connexion') 
def dashart(request):
    # utilisateur doit etre connecte
    if not request.user.is_authenticated:
        messages.warning(request, "Vous devez être connecté pour accéder à votre tableau de bord.")
        return redirect('connexion')          # ou 'controlArt' si tu veux

    # 2. Vérification que l'utilisateur a bien un profil Artisan
    try:
        artisan = request.user.artisan
    except Artisan.DoesNotExist:
        messages.error(request, "Vous n'avez pas encore complété votre profil artisan.")
        return redirect('controlArt')

    # === Tout est OK ===
    demandes = Demande.objects.filter(categorie=artisan.metier_principal)
    devis = Devis.objects.filter(artisan=artisan.user)

    context = {
        'demandes': demandes,
        'devis': devis,
        'total_demandes': demandes.count(),
        'devis_envoye': devis.count(),
    }

    return render(request, 'dashart.html', {'context':context, 'demandes': demandes, 'devis':devis,})

############3 zone de vevis #####################
@login_required(login_url='connexion') 
def devis(request):
    return render(request, 'devis.html')

## creation du devis ##
@login_required(login_url='connexion') 
def creerdevis(request, demande_id):
    demande = get_object_or_404(Demande, id=demande_id)
    
    if request.method == "POST":
        montant = request.POST.get('montant')
        delai = request.POST.get('delai')
        message = request.POST.get('message')
        
        Devis.objects.create(
            demande=demande,
            artisan=request.user,
            delai=delai,
            montant=montant,
            message=message,
        )
        
        return redirect('dashart')

    return render(request, 'creerdevis.html', {'demande': demande})

## modifier un devis ##
@login_required(login_url='connexion') 
def modifierdevis(request):
    return render(request, 'modifierdevis.html')



# supprimer le devis
@login_required(login_url='connexion') 
def supprimerdevis(request, devis_id):
    devis = get_object_or_404(Devis, id=devis_id)

    
    if devis.artisan == request.user:
        devis.delete()

    return redirect('dashart')


# modification du devis
def modifierdevis(request, devis_id):
    devis = get_object_or_404(Devis, id=devis_id)

    if devis.artisan != request.user:
        return redirect('dashart')

    if request.method == "POST":
        devis.montant = request.POST.get('montant')
        devis.delai = request.POST.get('delai')
        devis.message = request.POST.get('message')
        devis.save()

        return redirect('dashart')

    return render(request, 'modifierdevis.html', {'devis': devis})

## liste des demandes
@login_required(login_url='connexion') 
def listeDemandes(request):
    demandes = Demande.objects.all().order_by('-date_creation')
    return render(request, 'listedemandes.html', {'demandes': demandes})

# /////inscription pour les artisan

@login_required(login_url='connexion') 
def controlArt(request):
    try:
        request.user.artisan
        return redirect('dashart')
    except Artisan.DoesNotExist:
        pass

    form = InscriptionPro(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            try:
                with transaction.atomic():
                    artisan = form.save(commit=False)
                    artisan.user = request.user
                    if artisan.telephone1:
                        artisan.telephone1 = ''.join(filter(str.isdigit, artisan.telephone1))[-9:]  # garde les 9 derniers chiffres
                    if artisan.telephone2:
                        artisan.telephone2 = ''.join(filter(str.isdigit, artisan.telephone2))[-9:]
                    artisan.save()

                    
                    if hasattr(request.user, 'profil'):
                        request.user.profil.is_artisan = True
                        request.user.profil.save()

                messages.success(request, "✅ Votre profil artisan a été créé avec succès !")
                return redirect('dashart')

            except Exception as e:
                print("ERREUR SAVE ARTISAN:", e)
                messages.error(request, f"Erreur lors de l'enregistrement : {str(e)}")
        else:
            print("Erreurs du formulaire :", form.errors)
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")

    return render(request, 'controlArt.html', {'form': form})
    
    
def deconnexion(request):
    logout(request)
    return redirect( 'home')



# notification
# Notification.objects.create(
#     user=Demande.user,  
#     titre="Nouveau devis",
#     message=f"Vous avez reçu un devis pour '{Demande.titre}'",
#     type="warning"
# )