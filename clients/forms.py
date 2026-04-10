from django import forms
from .models import Demande
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

# tout ce qui est utile pour inscription
class RegisterForm(forms.Form):
    nom = forms.CharField(max_length=50, required=True)
    prenom = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    telephone = forms.CharField(max_length=13, required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    is_artisan = forms.BooleanField(required=False)
    accept_policy = forms.BooleanField(required=True, error_messages={
    'required': "Vous devez accepter la politique"
})
    
    # methode pour valider plusieurs champs a la fois
    def clean(self):
        cleaned_data = super().clean()
        
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password != confirm_password:
            self.add_error("confirm_password", "Les mots de passe ne sont pas identiques")
        return cleaned_data
    
    # methode pour verifier et valider l'email avec django
    def clean_email(self):
        email = self.cleaned_data.get("email")
        
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email existe déjà")
        
        return email
    # methode pour valider le mot de passe avec django
    def clean_password(self):
        password = self.cleaned_data.get("password")
        validate_password(password)
        return password
    
    
# zone des demandes de devis
class DemandeForm(forms.ModelForm):
    class Meta:
        model = Demande
        fields = ['titre', 'description', 'categorie', 'budget_min', 'budget_max', 'localisation']