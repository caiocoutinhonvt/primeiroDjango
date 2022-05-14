from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.db.models import Sum, Q, Avg, FloatField

from .models import Transaction, Category, Profile
from .forms import TransactionForm, CategoryForm, ProfileForm

from decimal import Decimal
from django.contrib import messages
import django_filters



# Create your views here.




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





# LIST TRANSACTION
def list(request):
    if request.user.is_authenticated:
        transaction = Transaction.objects.filter(user=request.user)
        price = transaction.aggregate(Sum('price')).get('price__sum') or Decimal(0.0)
        current_profile = Profile.objects.filter(user=request.user)
        
        profile = current_profile.last()
        category = TransactionForm 
        category_list = Category.objects.filter(user=request.user)

        if current_profile.exists():
            current_profile = True

        else:
            current_profile = False

        #######
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        if start_date and end_date:
            transaction = transaction.filter(
                date__range=[start_date, end_date]
          
            )
        
        #########
        filtered_category = None
        if request.POST.get("filter_category", None):
            filtered_category = Category.objects.get(pk=request.POST.get('filter_category', None))
            transaction = transaction.filter(category_id=request.POST.get('filter_category'))

     
        
        if profile is None:
            limit_month = Decimal(0.0)

        else:
            limit_month = profile.limit_month
        
        remaining = limit_month - price 

        context = {
            "transaction": transaction, 
            "price": price,
            'limit_month': limit_month,
            'remaining': remaining,
            'profile': profile,
            'category': category,
            'filters': {
                'category_filter': filtered_category
            },
            'category_list': category_list,
            'current_profile': current_profile
            
        }

        
        return render(request,'contas/listagem.html', context)
        
    else:
        return HttpResponseRedirect('/accounts/login')





# CREATE TRANSACTION
def create(request): 
    if request.user.is_authenticated:                                     
        data = {}
        
        user_id = request.user.id
        form = TransactionForm(request.POST, user_id=user_id) 
        data['form'] = form
        if form.is_valid():

            category = Category.objects.get(pk=request.POST['category'])
            category_total_value = category.transaction\
                .filter(date__month=4, date__year=2022)\
                .aggregate(Sum('price'))\
                .get('price__sum') or 0

            if category.limit_month < (category_total_value + Decimal(request.POST['price']) ):
                error = f"Despesa ultrapassa o valor limite mensal de R$ {category.limit_month} da categoria: {category.name}"
                data['error'] = error
                return render(request, 'contas/form.html', data)


            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Profile details updated.')
            return redirect('url_list')

    else:
        return HttpResponseRedirect('/accounts/login')
        

    return render(request, 'contas/form.html', data)




#UPDATE TRANSACTION
def update(request, id):
    if request.user.is_authenticated:
        data = {}
        transaction = Transaction.objects.get(id=id)
        user_id = request.user
        form = TransactionForm(request.POST or None, instance=transaction, user_id=user_id)
        data['form'] = form
        data['transaction'] = transaction
    
     
        if form.is_valid():

            category = Category.objects.get(pk=request.POST['category'])
            category_total_value = category.transaction\
                .filter(date__month=4, date__year=2022)\
                .exclude(pk=id)\
                .aggregate(Sum('price'))\
                .get('price__sum') or 0

            
            if category.limit_month < (category_total_value + Decimal(request.POST['price']) ):
                error = f"Despesa ultrapassa o valor limite mensal de R$ {category.limit_month} da categoria: {category.name}"
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
        transaction_color = Category.objects.filter(user=request.user)
       
        cats = Category.objects.filter(user=request.user)

        transactions=[]



        for cat in cats: 
            transaction = cat.transaction.count()
            transactions.append(transaction)


        data = {
                'category': cats,
                'transactions': transactions,
                'transaction_color': transaction_color,
               }
        
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

        else:
            error = "Nome ja adicionado em categoria"               

        data['form'] = form
        data['error'] = error
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
        data ['category'] = Category.objects.filter(user=request.user)
        
        return render(request,'contas/category.html', data)
        
    else:
        return HttpResponseRedirect('/accounts/login')
        



# DELETE CATEGORY
def delete_category(request, id):
    category = Category.objects.get(id=id)
    category.delete()
        
    return redirect('url_list_category') 




# EDIT PROFILE
def editprofile(request):
   
    if request.user.is_authenticated:                              
        data = {}
        
        profile = Profile.objects.get(user=request.user)
        form = ProfileForm(instance=profile)

        if request.method == 'POST':
           
          
            form = ProfileForm(request.POST or None,request.FILES, instance=profile)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user
                task.save()
                print('foi')
                return redirect('url_profile')

        data['form'] = form
        data['profile'] = profile
     
    else:
        return HttpResponseRedirect('/accounts/login')
     
    return render(request, 'contas/create_profile.html', data)   




# VIEW PROFILE     
def profile(request):
    current_profile = Profile.objects.filter(user=request.user)

    if current_profile.exists():
        data = {}
        data ['profile'] = Profile.objects.get(user=request.user)
    else:
        return redirect("url_create_profile")

    # if profile is None:
    #     return HttpResponseRedirect('/create_profile')
    
    return render(request,'contas/profile.html', data)




# CREATE PROFILE 
def createprofile(request):
    if request.user.is_authenticated:                                     
        data = {}
        form = ProfileForm(request.POST or None, request.FILES)

       
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            print('foi')
            return redirect('url_profile')
            

                     

        data['form'] = form
    else:
        return HttpResponseRedirect('/accounts/login')
     
    return render(request, 'contas/create_profile.html', data)
    
    

        




              
       
  
     
        