from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.db.models import Sum, Q, Avg, FloatField

from .models import Transaction, Category, Profile
from .forms import TransactionForm, CategoryForm, ProfileForm

from decimal import Decimal



# Create your views here.

def login(request):
    pass




# MONTH VALUE 
def limit_month(request, id):
   
    if request.user.is_authenticated:
        data = {}
        userchoices = Profile.objects.get(id=id)
        form = ProfileForm(request.POST or None, instance=userchoices)

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            print('foi')
            return redirect('url_list')

        data['form'] = form
        data['limit_month'] = userchoices
    return render(request, 'contas/limit_month.html', data)



# LIST 
def list(request):
    if request.user.is_authenticated:
       
        transaction = Transaction.objects.filter(user=request.user)
        price = transaction.aggregate(Sum('price')).get('price__sum') or 0
        limit_month_obj = Profile.objects.filter(user=request.user).last() or 0
        if limit_month_obj is None:
            limit_month = 0.0

        else:
            limit_month = limit_month_obj.limit_month
       
        
        
        
        remaining = limit_month - price 

        context = {
            "transaction": transaction, 
            "price": price,
            'limit_month': limit_month,
            'remaining': remaining,
            'limit_month_obj': limit_month_obj,
        }

        
        return render(request,'contas/listagem.html', context)
        
    else:
        return HttpResponseRedirect('/accounts/login')


# CREATE TRANSACTION
def create(request): 
    if request.user.is_authenticated:                                     
        data = {}
        form = TransactionForm(request.POST) 
        data['form'] = form
        if form.is_valid():

            category = Category.objects.get(pk=request.POST['category'])
            category_total_value = category.transaction_set\
                .filter(date__month=4, date__year=2022)\
                .aggregate(Sum('price'))\
                .get('price__sum') or 0

            if category.limit_month < (category_total_value + Decimal(request.POST['price']) ):
                error = f"nâo foi possível criar a atransação pois atingiu o limite mensal da categoria {category.name} de: {category.limit_month}"
                data['error'] = error
                return render(request, 'contas/form.html', data)


            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('url_list')

    else:
        return HttpResponseRedirect('/accounts/login')
        

    return render(request, 'contas/form.html', data)

#UPDATE TRANSACTION
def update(request, id):
    if request.user.is_authenticated:
        data = {}
        transaction = Transaction.objects.get(id=id)
        form = TransactionForm(request.POST or None, instance=transaction)
        data['form'] = form
        data['transaction'] = transaction
    
     
        if form.is_valid():

            category = Category.objects.get(pk=request.POST['category'])
            category_total_value = category.transaction_set\
                .filter(date__month=4, date__year=2022)\
                .exclude(pk=id)\
                .aggregate(Sum('price'))\
                .get('price__sum') or 0

            
            if category.limit_month < (category_total_value + Decimal(request.POST['price']) ):
                error = f"nâo foi possível criar a atransação pois atingiu o limite mensal da categoria {category.name} de: {category.limit_month}"
                data['error'] = error
                return render(request, 'contas/form.html', data)

            task = form.save(commit=False)
            task.user = request.user
            task.save()
            print('foi')
            return redirect('url_list')
    return render(request, 'contas/form.html', data)



# DELETE TRANSCATION
def delete(request, id):
    transaction = Transaction.objects.get(id=id)
    transaction.delete()
        
    return redirect('url_list') 


# CHARTS
def charts(request):
    if request.user.is_authenticated:
        data = {'transactions': Transaction.objects.all().count(),
                'transaction_d': Transaction.objects.filter(category_id = 1, user=request.user).count(),
                'transaction_a': Transaction.objects.filter(category_id = 3, user= request.user).count(),
                'transaction_t' : Transaction.objects.filter(category_id = 2, user =request.user).count()}
        
        return render(request, 'contas/charts.html', data)
    else:
        return HttpResponseRedirect('/accounts/login')


#CREATE CATEGORY
def create_category(request):
    if request.user.is_authenticated:                                     
        data = {}
        form = CategoryForm(request.POST or None)

       
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            print('foi')
            return redirect('url_list_category')

                         

        data['form'] = form
    else:
        return HttpResponseRedirect('/accounts/login')
     
    return render(request, 'contas/category_form.html', data)
    
# UPDATE CATEGORY 
def update_category(request, id):
    if request.user.is_authenticated:
        data = {}
        category = Category.objects.get(id=id)
        form = CategoryForm(request.POST or None, instance=category)

    
     
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            print('foi')
            return redirect('url_list_category')

        data['form'] = form
        data['category'] = category
    return render(request, 'contas/category_form.html', data)




# LIST CATEGORY
def list_category(request):
    if request.user.is_authenticated:
        data = {}
        data ['category'] = Category.objects.all()
        
        return render(request,'contas/category.html', data)
        
    else:
        return HttpResponseRedirect('/accounts/login')
        


# DELETE CATEGORY
def delete_category(request, id):
    category = Category.objects.get(id=id)
    category.delete()
        
    return redirect('url_list_category') 


 


# DASHBOARD 
def dashboard(request):
    data = {'transaction': Transaction.objects.all().count(),
            'transaction_d': Transaction.objects.filter(category_id = 1, user=request.user).count(),
            'transaction_a': Transaction.objects.filter(category_id = 3, user= request.user).count(),
            'transaction_t' : Transaction.objects.filter(category_id = 2, user =request.user).count(),
            'total_price': Transaction.objects.filter(user=request.user).aggregate(Sum('price')).get('price__sum')}

    return render(request,'contas/dashboard.html', data)  