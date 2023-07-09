from django.shortcuts import render, redirect
from perfil.models import mCategoria, mConta
from .models import mValores
from django.contrib import messages
from django.contrib.messages import constants
from django.http import HttpResponse
from datetime import datetime


# Create your views here.
def novo_valor(request):
    if request.method == 'GET':
        contas = mConta.objects.all()
        categorias = mCategoria.objects.all()

        return render(request, 'novo_valor.html', {'contas': contas, 'categorias': categorias})
    
    elif request.method == 'POST':
        valor = request.POST.get('valor')
        categoria = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        data = request.POST.get('data')
        conta = request.POST.get('conta')
        tipo = request.POST.get('tipo')

        valores = mValores(
            valor = valor,
            categoria_id = categoria,
            descricao = descricao,
            data = data,
            conta_id = conta,
            tipo = tipo
        )

        valores.save()

        conta = mConta.objects.get(id=conta)
        
        if tipo == 'E':
            conta.valor += int(valor)
            messages.add_message(request, constants.SUCCESS, 'Entrada salva com sucesso.')
        elif tipo == 'S':
            conta.valor -= int(valor)
            messages.add_message(request, constants.WARNING, 'Saida salva com sucesso.')

        conta.save()


        return redirect('/extrato/novo_valor')
    
def view_extrato(request):
    contas = mConta.objects.all()
    categorias = mCategoria.objects.all()

    conta_get = request.GET.get('conta')
    categoria_get = request.GET.get('categoria')

    valores = mValores.objects.filter(data__month=datetime.now().month)

    if conta_get:
        valores = valores.filter(conta__id=conta_get)

    if categoria_get:
        valores = valores.filter(categoria__id=categoria_get)

    return render(request, 'view_extrato.html', {'valores': valores, 'contas': contas, 'categorias': categorias})