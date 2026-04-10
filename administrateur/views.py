from django.shortcuts import render

# Create your views here.

def admins(request):
    return render(request, 'admins.html')

def utilisateurs(request):   
    return render(request, 'utilisateurs.html')