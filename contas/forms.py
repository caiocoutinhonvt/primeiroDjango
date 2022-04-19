from django.forms import ModelForm
from .models import Transacao
from django import forms



class TransacaoForm(ModelForm):
    class Meta:
        model = Transacao
      
        fields = ['data', 'descricao', 'valor', 'categoria']

        widgets = {
            'data': forms.SelectDateWidget( attrs={
                                                'class': 'form-control datetimepicker-input',
                                                'data-target': 'datetimepicker1',
                                                'data-mask': 'data-mask',}),
            'valor': forms.NumberInput(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'})
        }
        