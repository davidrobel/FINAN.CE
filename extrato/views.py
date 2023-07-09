from django.shortcuts import render, redirect
from perfil.models import mCategoria, mConta
from .models import mValores
from django.contrib import messages
from django.contrib.messages import constants
from django.http import HttpResponse, FileResponse
from datetime import datetime, date
from django.template.loader import render_to_string
import os
from django.conf import settings
from weasyprint import HTML #para gerar PDFs apartir do html
from io import BytesIO #permite salvar bytes em memoria ao inves de salvar em disco


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


def exportar_pdf(request): #usando weasyprint: pip install weasyprint
    valores = mValores.objects.filter(data__month=datetime.now().month)

    path_template = os.path.join(settings.BASE_DIR, 'templates/partials/extrato.html')
    template_render = render_to_string(path_template, {'valores': valores})


    path_output = BytesIO()
    HTML(string=template_render).write_pdf(path_output)

    path_output.seek(0)

    data_atual = date.today().strftime('%d_%m_%Y')

    
    return FileResponse(path_output, filename= data_atual + "_Extrato.pdf")