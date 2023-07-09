from django.shortcuts import render, redirect
from perfil.models import mCategoria, mConta
from .models import mValores
from django.contrib import messages
from django.contrib.messages import constants
from django.http import HttpResponse


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