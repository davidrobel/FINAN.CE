from django.shortcuts import render
from perfil.models import mCategoria
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from perfil.utils import saldo_despesas, calcula_total
from extrato.models import mValores
from datetime import datetime

# Create your views here.
def definir_planejamento(request):
    categorias = mCategoria.objects.all()

    return render(request, 'definir_planejamento.html', {'categorias': categorias})


@csrf_exempt
def update_valor_categoria(request, id):
    corpo = json.load(request)['novo_valor']
    categoria = mCategoria.objects.get(pk=id)
    categoria.valor_planejamento = corpo
    categoria.save()
    return JsonResponse({'status': 'Sucesso'})


def ver_planejamento(request):
    categorias = mCategoria.objects.all()
    saida_mes = mValores.objects.filter(data__month=datetime.now().month).filter(tipo='S')
    entrada_mes = mValores.objects.filter(data__month=datetime.now().month).filter(tipo='E')

    total_entrada_mes = calcula_total(entrada_mes, 'valor')    
    total_saida_mes = calcula_total(saida_mes, 'valor')

    percentual_saida_mes = total_saida_mes * 100 / total_entrada_mes

    
    return render(request, 'ver_planejamento.html', {'categorias': categorias, 
                                                     'total_saida_mes': total_saida_mes, 
                                                     'total_entrada_mes': total_entrada_mes,
                                                     'percentual_saida_mes': int(percentual_saida_mes)})