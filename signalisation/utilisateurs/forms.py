from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Utilisateur

class UtilisateurCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    
    # Filtrer les choix pour exclure le rôle administrateur
    FILTERED_ROLES = [choice for choice in Utilisateur.ROLES if choice[0] != 'admin']
    role = forms.ChoiceField(choices=FILTERED_ROLES)
    
    phone = forms.CharField(required=False)
    adresse = forms.CharField(required=False)
    date_naissance = forms.DateField(required=False)

    class Meta:
        model = Utilisateur
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 
                 'phone', 'adresse', 'date_naissance', 'password1', 'password2')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['first_name', 'last_name', 'email', 'phone', 'adresse', 'date_naissance']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Prénom'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Téléphone'
            }),
            'adresse': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Adresse'
            }),
            'date_naissance': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }