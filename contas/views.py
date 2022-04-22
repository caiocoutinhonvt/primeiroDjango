from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect

from .models import Transacao
from .forms import TransacaoForm
from django.db.models import Sum
from django.contrib import messages



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
            print('foi')
            return redirect('url_listagem')

                         

        data['form'] = form
    else:
        return HttpResponseRedirect('/accounts/login')
        

    return render(request, 'contas/form.html', data)

#UPDATE
def update(request, id):
    if request.user.is_authenticated:
        data = {}
        transacao = Transacao.objects.get(id=id)
        form = TransacaoForm(request.POST or None, instance=transacao)

    
     
        if form.is_valid():
            form.save()
            print('foi')
            return redirect('url_listagem')

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
        data = {'transacoes': Transacao.objects.all().count(),
                'transacoes_d': Transacao.objects.filter(categoria_id = 1).count(),
                'transacoes_a': Transacao.objects.filter(categoria_id = 2).count(),
                'transacoes_t' : Transacao.objects.filter(categoria_id = 3).count() }
        
        return render(request, 'contas/charts.html', data)
    else:
        return HttpResponseRedirect('/accounts/login')