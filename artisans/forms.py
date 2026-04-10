from django import forms
from .models import Artisan, Devis

class DevisForm(forms.ModelForm):
    class Meta:
        model = Devis
        fields = ['montant', 'delai', 'message']
        
        
class InscriptionPro(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

class InscriptionPro(forms.ModelForm):
    class Meta:
        model = Artisan
        fields = [
            'date_naissance', 'sexe', 'cni', 'nationalite',
            'telephone1', 'telephone2',
            'metier_principal', 'annees_experiences', 'niveau_formation',
            'registre_commercial', 'description',
            'cni_recto', 'cni_verso', 'attestation', 'photo_profil_pro',
            'ville_principale', 'quartier_intervention', 'rayon',
            'adresse', 'disponibilite',
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['telephone1'].widget.attrs.update({
            'placeholder': '+237 6XX XX XX XX',
            'maxlength': '15'
        })
        self.fields['telephone2'].widget.attrs.update({
            'placeholder': '+237 6XX XX XX XX',
            'maxlength': '15'
        })
    
    
    