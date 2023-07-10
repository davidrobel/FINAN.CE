from django.shortcuts import render
from perfil.models import mCategoria
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

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