from django import forms
from core.models import Usuario
from django.contrib.auth.forms import UserCreationForm


class UserAdminCreationForm(UserCreationForm):

    class Meta:
        model = Usuario
        fields = [
            'username', 'tipo', 'cpf_cnpj', 'email'
        ]

class UserAdminForm(forms.ModelForm):
    
    class Meta:
        model = Usuario
        fields = [
            'username', 'is_staff', 'is_active', 'is_superuser', 'is_anonymous', 'is_trusty', 'tipo', 'nome_fantasia',
             'razao_social', 'cpf_cnpj', 'data_nascimento', 'sexo', 'telefone', 'email', 'last_login'
        ]
