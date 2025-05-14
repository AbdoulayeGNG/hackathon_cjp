from django import forms
from .models import Report

class ReportForm(forms.ModelForm):
    location_lat = forms.DecimalField(widget=forms.HiddenInput(attrs={'id': 'id_location_lat'}))
    location_lng = forms.DecimalField(widget=forms.HiddenInput(attrs={'id': 'id_location_lng'}))
    
    class Meta:
        model = Report
        fields = ['title', 'category', 'description', 'image', 'location_lat', 'location_lng', 'address']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Donnez un titre à votre signalement'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Décrivez le problème en détail'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'address': forms.HiddenInput(attrs={'id': 'id_address'})
        }

    def clean(self):
        cleaned_data = super().clean()
        lat = cleaned_data.get('location_lat')
        lng = cleaned_data.get('location_lng')

        if not lat or not lng:
            raise forms.ValidationError("Veuillez sélectionner un emplacement sur la carte")

        return cleaned_data