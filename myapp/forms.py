from django.forms import ModelForm
from .models import Transaction
from django import forms



class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
      
        fields = ['date', 'description', 'price', 'category']

        widgets = {
            'date': forms.DateInput( attrs={ 'class': 'form-control date',}),
            'price': forms.TextInput(attrs={'class':'form-control money ', 'type':'text'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }
        