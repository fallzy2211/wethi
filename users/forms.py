from django import forms
from .models import Offer
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['ma_devise', 'devise_souhaitee', 'taux_souhaite', 'quantite']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username', 'email', 'type',
            'piece_identite',
            'numero_agrement', 'document_agrement',
            'password1', 'password2'
        ]

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('type')
        numero_agrement = cleaned_data.get('numero_agrement')
        document_agrement = cleaned_data.get('document_agrement')

        # Validation spécifique pour les cambistes
        if user_type == 'cambiste':
            if not numero_agrement:
                self.add_error('numero_agrement', "Le numéro d’agrément est obligatoire pour les cambistes.")
            if not document_agrement:
                self.add_error('document_agrement', "Le document d’agrément (photo) est obligatoire pour les cambistes.")
        return cleaned_data
