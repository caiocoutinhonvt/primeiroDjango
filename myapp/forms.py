from django.forms import ModelForm
from .models import Transaction, Category, Profile
from django import forms




class ProfileForm(ModelForm):
    class Meta:
        model = Profile

        fields = ['limit_month']

        widgets = {


            'limit_month': forms.TextInput(attrs={'class':'form-control money ', 'type':'text'}),
        }

            



class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
      
        fields = ['date', 'description', 'price', 'category']
        

        widgets = {
            'date': forms.DateInput( attrs={ 'class': 'form-control date'}),
            'price': forms.TextInput(attrs={'class':'form-control money ', 'type':'text'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }
        

class CategoryForm(ModelForm):
    class Meta:
        model = Category    
      
        fields = ['name', 'limit_month',]

        widgets = {

            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'limit_month': forms.TextInput(attrs={'class':'form-control money ', 'type':'text'})

        }