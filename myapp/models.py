from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

# Create your models here.

class SexOptions(models.TextChoices):
    FEMININO = 'Feminino'
    MASCULINO = 'Masculino'
    OUTROS = 'OUTROS'

   
        
    

class Profile(models.Model):
    
    limit_month = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(get_user_model(), on_delete= models.CASCADE, related_name='user_profile')
    profile_pic = models.ImageField(upload_to= "images/profile/", default = 'default.svg', null=True, blank=True)
    name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices= SexOptions.choices)
    email = models.EmailField()
    phone = models.CharField(max_length=60, null=True, blank=True)
    adress = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    cep = models.IntegerField()


    def __str__(self):
        return self.name
    
   
    



class Category(models.Model):
    name = models.CharField('nome', max_length=100, unique= True)
    dt_creation = models.DateTimeField(auto_now_add= True)
    limit_month = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    color = models.CharField(max_length=7)
    

    def __str__(self):
        return self.name


class Transaction(models.Model):
    
    date = models.DateTimeField()
    description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='transaction')    
    user = models.ForeignKey(get_user_model(), on_delete= models.CASCADE)
    

    class Meta:
        verbose_name_plural = "Transactions"
    
    def __str__(self):
        return self.description

   
  