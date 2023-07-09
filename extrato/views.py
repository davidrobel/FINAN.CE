from django.shortcuts import render
from perfil.models import mCategoria, mConta

# Create your views here.
def novo_valor(request):
    if request.method == 'GET':
        contas = mConta.objects.all()
        categoria = mCategoria.objects.all()

        return render(request, 'novo_valor.html', {'contas': contas, 'categoria': categoria})
    
