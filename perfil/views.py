from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import mConta, mCategoria
from django.contrib import messages
from django.contrib.messages import constants
from .utils import calcula_total, calcula_equilibrio_financerio, saldo_despesas
from extrato.models import mValores
from datetime import datetime

# Create your views here.
def home (request):
    contas = mConta.objects.all()
    valores = mValores.objects.filter(data__month=datetime.now().month)
    entradas = valores.filter(tipo='E')
    saidas = valores.filter(tipo='S')

    total_entradas = calcula_total(entradas, 'valor')
    total_saidas = calcula_total(saidas, 'valor')
    percentual_gastos_essenciais, percentual_gastos_nao_essenciais = calcula_equilibrio_financerio()

    total_entrada_mes, total_saida_mes, total_livre = saldo_despesas()
    
    total_contas = calcula_total(contas, 'valor')

    return render(request, 'home.html', {'contas': contas, 
                                         'total_contas':total_contas, 
                                         'total_saidas':total_saidas, 
                                         'total_entradas': total_entradas,
                                         'percentual_gastos_essenciais': int(percentual_gastos_essenciais),
                                         'percentual_gastos_nao_essenciais': int(percentual_gastos_nao_essenciais),
                                         'total_entrada_mes' : total_entrada_mes,
                                         'total_saida_mes': total_saida_mes,
                                         'total_livre': total_livre})



def gerenciar(request):
    categoria = mCategoria.objects.all()

    contas = mConta.objects.all()

    total_contas = calcula_total(contas, 'valor')

    return render(request, 'gerenciar.html', {'contas':contas, 'total_contas':total_contas, 'categorias':categoria})

def cadastrar_banco(request):
    #pega dados do formulario html e atribui a variaveis
    apelido = request.POST.get('apelido')
    banco = request.POST.get('banco')
    tipo = request.POST.get('tipo')
    valor = request.POST.get('valor')
    icone = request.FILES.get('icone')

    if len(apelido.strip()) == 0 or len(valor.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
        return redirect('/perfil/gerenciar/')

    # associa o valor do candpo html com as variaveis acima dentro da instacia nova_conta
    nova_conta = mConta(
        apelido = apelido,
        banco = banco,
        tipo = tipo,
        valor = valor,
        icone = icone
    )
    #salva dados no banco de dados
    nova_conta.save()

    messages.add_message(request, constants.SUCCESS, 'Salvo com sucesso')
    
    return redirect('/perfil/gerenciar/')


def deletar_banco(request, id):
    conta = mConta.objects.get(pk=id)
    conta.delete()

    messages.add_message(request, constants.SUCCESS, 'Conta deletada com sucesso!')
    return redirect('/perfil/gerenciar/')

def cadastrar_categoria(request):

    nome = request.POST.get('categoria')
    essencial = bool(request.POST.get('essencial'))

    categoria = mCategoria(
        categoria = nome,
        essencial = essencial
    )

    categoria.save()

    messages.add_message(request, constants.SUCCESS, 'Categoria salvo')

    return redirect('/perfil/gerenciar/')


def update_categoria(request, id):

    categoria = mCategoria.objects.get(id=id)
    categoria.essencial =  not categoria.essencial
    categoria.save()

    return redirect('/perfil/gerenciar/')


def dashboard(request):
    dados = {}

    categorias = mCategoria.objects.all()

    for i in categorias:
        total = 0
        valores = mValores.objects.filter(categoria=i)
        for v in valores:
            total += v.valor

        dados[i.categoria] = total

    return render(request, 'dashboard.html', {'labels': list(dados.keys()), 'values': list(dados.values())})