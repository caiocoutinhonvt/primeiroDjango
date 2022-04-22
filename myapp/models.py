from django.db import models

# Create your models here.




class Category(models.Model):
    name = models.CharField(max_length=100)
    dt_creation = models.DateTimeField(auto_now_add = True)


    def __str__(self):
        return self.name


class Transaction(models.Model):
    
    date = models.DateTimeField()
    description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Transações"
    
    def __str__(self):
        return self.description

   
  