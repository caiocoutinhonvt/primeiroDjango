from django.forms import ModelForm
from .models import Transacao
from django import forms



class TransacaoForm(ModelForm):
    class Meta:
        model = Transacao
      
        fields = ['data', 'descricao', 'valor', 'categoria']

        widgets = {
            'data': forms.DateInput( attrs={ 'class': 'form-control date',}),
            'valor': forms.TextInput(attrs={'class':'form-control money ', 'type':'text'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'})
        }
        