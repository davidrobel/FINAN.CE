from django.shortcuts import render, redirect
from django.urls import reverse
from perfil.models import mCategoria
from .models import mContaPagar, mContaPaga
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime
from django.contrib import messages
from django.contrib.messages import constants


# Create your views here.
def definir_contas(request):
    if request.method == 'GET':
        categorias = mCategoria.objects.all()

        return render(request, 'definir_contas.html', {'categorias': categorias})
    
    elif request.method == 'POST':
        titulo = request.POST.get('titulo')
        categoria = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        dia_pagamento = request.POST.get('dia_pagamento')

        conta = mContaPagar(
            titulo = titulo,
            categoria_id = categoria, #colocar _id na variavel pois 'e referente a coluna ID da model do app perfil que se chama categoria_id
            descricao = descricao,
            valor = valor,
            dia_pagamento = dia_pagamento
        )

        conta.save()

        messages.add_message(request, constants.SUCCESS, 'Conta salva com sucesso!')

        return redirect('/contas/definir_contas/')
    

def ver_contas(request):
    if request.method == 'GET':
        MES_ATUAL= datetime.now().month
        DIA_ATUAL = datetime.now().day

        todas_contas = mContaPagar.objects.all()
        contas_pagas = mContaPaga.objects.filter(data_pagamento__month = MES_ATUAL).values('conta')       
        contas_vencidas = todas_contas.filter(dia_pagamento__lt = DIA_ATUAL).exclude(id__in = contas_pagas)        
        contas_prox_vencimento = todas_contas.filter(dia_pagamento__lte = DIA_ATUAL + 5).filter(dia_pagamento__gt = DIA_ATUAL).exclude(id__in = contas_pagas)
        restantes = todas_contas.exclude(id__in = contas_vencidas).exclude(id__in = contas_prox_vencimento).exclude(id__in = contas_pagas)
        
        return render(request, 'ver_contas.html', {'contas_vencidas': contas_vencidas, 
                                                   'contas_prox_vencimento': contas_prox_vencimento, 
                                                   'restantes':restantes})
    
def paga_conta(request, id):
    #paga_conta = mContaPagar.objects.get(pk=id)
    id = id
    data = datetime.now()

    valores = mContaPaga(
        conta_id = id,
        data_pagamento = data
    )

    valores.save()
    

    messages.add_message(request, constants.SUCCESS, 'UFA!! Conta paga.')
    return redirect('/contas/ver_contas/')