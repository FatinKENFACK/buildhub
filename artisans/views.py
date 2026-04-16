from datetime import timezone

from django.shortcuts import get_object_or_404, redirect, render

from notifications.models import Notification
from .forms import ArtisanEditForm, InscriptionPro
from clients.models import Demande
from artisans.models import Artisan, Devis
from django.contrib.auth import logout
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from decimal import ROUND_HALF_UP, Decimal
from django.contrib import messages

# tableau de board de l'artian
@login_required(login_url='connexion') 
def dashart(request):
    # utilisateur doit etre connecte
    if not request.user.is_authenticated:
        messages.warning(request, "Vous devez être connecté pour accéder à votre tableau de bord.")
        return redirect('connexion')

    # 2. Vérification que l'utilisateur a bien un profil Artisan
    try:
        artisan = request.user.artisan
    except Artisan.DoesNotExist:
        messages.error(request, "Vous n'avez pas encore complété votre profil artisan.")
        return redirect('controlArt')

    demandes = Demande.objects.filter(
         categorie__iexact=artisan.metier_principal.strip()
    )
    devis = Devis.objects.filter(artisan=artisan.user)

    notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).order_by('-created_at')[:5]

    context = {
        'demandes': demandes,
        'devis': devis,
        'total_demandes': demandes.count(),
        'devis_envoye': devis.count(),
        'notifications': notifications,
    }

    return render(request, 'dashart.html', 
        {
            'context':context, 
            'demandes': demandes, 
            'devis':devis, 
            'notifications': notifications,
         }
    )

############3 zone de vevis #####################
@login_required(login_url='connexion') 
def devis(request):

    # on recuper l'artisan connecte 
    if hasattr(request.user, 'artisan'):
        artisan = request.user.artisan
        devis = Devis.objects.filter(artisan=artisan.user)
    else:
        devis = Devis.objects.none()

    # calcul de la TVA
    devis_avec_tva = []
    for d in devis:
        tva = (d.montant * Decimal('0.20')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        total_ttc = (d.montant + tva).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        devis_avec_tva.append({
            'devis': d,
            'tva': tva,
            'total_ttc': total_ttc,
        })

    Notification.objects.filter(
        user=request.user,
        type='new_demande',
        is_read=False
    ).update(is_read=True)

    context = {
        'total_devis':devis.count(),
        'devis_attente': devis.filter(statut='attente').count(),
        'devis_refusé': devis.filter(statut='refusé').count(),
        'devis_accepté': devis.filter(statut='accepté').count(),
        'devis_avec_tva': devis_avec_tva 
    }

    return render(request, 'devis.html', context)

##```````````````` creation du devis ````````````````##
@login_required(login_url='connexion') 
def creerdevis(request, demande_id):

    demande = get_object_or_404(Demande, id=demande_id)
    artisan = request.user

    existe = Devis.objects.filter(demande=demande, artisan=artisan).exists()

    if existe:
        messages.error(request, "Vous avez déjà envoyé un devis pour cette demande. Vous pouvez juste la modifier")
        return redirect('listeDemandes')
    
    if request.method == "POST":
        montant = request.POST.get('montant')
        delai = request.POST.get('delai')
        message_text = request.POST.get('message')
        
        Devis.objects.create(
            demande=demande,
            artisan=request.user,
            delai=delai,
            montant=montant,
            message=message_text,
        )
        messages.success(request, f" Votre devis a été envoyé avec succès !")
        return redirect('dashart')
    
    return render(request, 'creerdevis.html', {'demande': demande})

## modifier un devis ##
@login_required(login_url='connexion') 
def modifierdevis(request):
    return render(request, 'modifierdevis.html')



# supprimer le devis
@login_required(login_url='connexion') 
def supprimerdevis(request, devis_id):
    devis = get_object_or_404(Devis, id=devis_id, artisan=request.user)

    if request.method == "POST":
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

    if hasattr(request.user, 'artisan'):
        artisan = request.user.artisan

        demandes = Demande.objects.filter(
            categorie__iexact=artisan.metier_principal.strip()
        ).order_by('-date_creation')

    else:
        demandes = Demande.objects.none()

    Notification.objects.filter(
        user=request.user,
        type='new_demande',
        is_read=False
    ).update(is_read=True)

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
                        artisan.telephone1 = ''.join(filter(str.isdigit, artisan.telephone1))[-9:]
                    if artisan.telephone2:
                        artisan.telephone2 = ''.join(filter(str.isdigit, artisan.telephone2))[-9:]
                    artisan.save()

                    
                    if hasattr(request.user, 'profil'):
                        request.user.profil.is_artisan = True
                        request.user.profil.save()

                messages.success(request, " Votre profil artisan a été créé avec succès !")
                return redirect('dashart')

            except Exception as e:
                print("ERREUR SAVE ARTISAN:", e)
                messages.error(request, f"Erreur lors de l'enregistrement : {str(e)}")
        else:
            print("Erreurs du formulaire :", form.errors)
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")

    return render(request, 'controlArt.html', {'form': form})

# edition du profil
def edit_artisan(request):
    try:
        artisan = request.user.artisan
    except Artisan.DoesNotExist:
        messages.error(request, "Vous n'avez pas encore de profil artisan.")
        return redirect('controlArt')

    form = ArtisanEditForm(request.POST or None, request.FILES or None, instance=artisan)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Votre profil a été mis à jour avec succès !")
            return redirect('dashart')
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")

    context = {
        'form': form,
        'artisan': artisan,
    }
    return render(request, 'edit_artisan.html', context)
    
    
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