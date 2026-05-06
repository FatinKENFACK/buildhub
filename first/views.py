from django.shortcuts import render
from artisans.models import Artisan

def homePage(request):
    
    artisan = Artisan.objects.all()
    plombier = Artisan.objects.filter(metier_principal='Plomberie')
    maçon = Artisan.objects.filter(metier_principal='Maçonnerie')
    electicite = Artisan.objects.filter(metier_principal='Électricité')
    menuisier = Artisan.objects.filter(metier_principal='Menuiserie')
    peintre = Artisan.objects.filter(metier_principal='Peinture')
    carrelage = Artisan.objects.filter(metier_principal='Carrelage')
    elect = Artisan.objects.filter(metier_principal='Électricité')

    context = {
        'artisan': artisan.count(),
        'plombier': plombier.count(),
        'maçon': maçon.count(),
        'electicite': electicite.count(),
        'menuisier': menuisier.count(),
        'peintre': peintre.count(),
        'carrelage': carrelage.count(),
        'elect': elect.count(),

    }

    return render(request, 'home.html', context)







