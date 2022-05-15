from django.forms import ModelForm
from .models import Transaction, Category, Profile
from django import forms
from django.conf import settings





class ProfileForm(ModelForm):
    class Meta:
        model = Profile

        fields = {'limit_month', 'name', 'last_name', 'gender', 'email', 'phone', 'adress', 'city', 'cep', 'profile_pic'}
        exclude = {'user',}
        widgets = {


            'limit_month': forms.NumberInput(attrs={'class':'form-control money', 'type':'int'}),
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'profile_pic': forms.FileInput(attrs={'class':'form-control'}),
            'gender': forms.Select(attrs={'class':'form-control'}),
            'email': forms.TextInput(attrs={'class':'form-control'}),
            'phone': forms.TextInput(attrs={'class':'form-control'}),
            'adress': forms.TextInput(attrs={'class':'form-control'}),
    
            'city': forms.TextInput(attrs={'class':'form-control'}),
            'cep' :forms.NumberInput(attrs={'class':'form-control','placeholder':'Digite seu CEP'}),

        }

            



class TransactionForm(ModelForm):
    
    # date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS,
    #                                     widget=forms.DateInput(
    #                                         format="%d/%m/%Y",
    #                                         attrs={
    #                                             'placeholder': 'digite sua data',  
    #                                             'class': 'form-control', 
    #                                             'type': 'date',
    #                                         }
    #                                     ))

    class Meta:
        model = Transaction
      
        fields = ['date', 'description', 'price', 'category']
        

        widgets = {
            'date': forms.DateInput( attrs={ 'placeholder': 'digite sua data', 'class': 'form-control date', 'type': 'date'}),
            'price': forms.TextInput(attrs={'class':'form-control money ', 'type':'text'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite sua descrição'}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, user_id, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)

        categories = Category.objects.filter(user_id=user_id)
        
        self.fields['category'].queryset = categories
                


        

class CategoryForm(ModelForm):
    class Meta:
        model = Category    
      
        fields = ['name', 'limit_month', 'color',]

        widgets = {

            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'limit_month': forms.TextInput(attrs={'class':'form-control money ', 'type':'text'}),
            'color': forms.TextInput(attrs={'class':'form-control form-control-color' ,'type': 'color', 'width': '4px'})

        }

 
        
