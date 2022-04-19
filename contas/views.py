from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import datetime
from .models import Transacao
from .forms import TransacaoForm
from django.db.models import Sum



# Create your views here.

def login(request):
    pass

#READ
def listagem(request):
    if request.user.is_authenticated:
        data = {}
        data ['transacoes'] = Transacao.objects.all()
        return render(request,'contas/listagem.html', data)
    else:
        return HttpResponseRedirect('/accounts/login')


#CREATE
def nova_transacao(request): 
    if request.user.is_authenticated:                                     
        data = {}
        form = TransacaoForm(request.POST or None)

        if form.is_valid():
            form.save()
            return redirect('url_listagem')                 #retorna para a pagina listagem

        data['form'] = form
    else:
        return HttpResponseRedirect('/accounts/login')
        

    return render(request, 'contas/form.html', data)

#UPDATE
def update(request, id):
    
    data = {}
    transacao = Transacao.objects.get(id=id)
    form = TransacaoForm(request.POST or None, instance=transacao)

    if form.is_valid():
        form.save()
        return redirect('url_listagem')                 #retorna para a pagina listagem

    data['form'] = form
    data['transacao'] = transacao
    return render(request, 'contas/form.html', data)



# DELETE
def delete(request, id):
    transacao = Transacao.objects.get(id=id)
    transacao.delete()
        
    return redirect('url_listagem') 


def charts(request):
    if request.user.is_authenticated:
        data = {
            'graph':[500, 25, 250]
        }
        
        return render(request, 'contas/charts.html', data)
    else:
        return HttpResponseRedirect('/accounts/login')