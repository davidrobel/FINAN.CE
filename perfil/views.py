from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import mConta, mCategoria
from django.contrib import messages
from django.contrib.messages import constants
from .utils import calcula_total

# Create your views here.
def home (request):
    contas = mConta.objects.all()

    total_contas = calcula_total(contas, 'valor')

    return render(request, 'home.html', {'contas': contas, 'total_contas':total_contas})



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