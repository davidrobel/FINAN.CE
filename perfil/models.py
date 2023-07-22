from django.db import models
from datetime import datetime

# Create your models here.
class mCategoria(models.Model):
    categoria = models.CharField(max_length=50)
    essencial = models.BooleanField(default=False)
    valor_planejamento = models.FloatField(default=0)


    def __str__(self):
        return self.categoria
    
    def total_gasto(self):
        from extrato.models import mValores
        from .utils import calcula_total
        valores = mValores.objects.filter(categoria__id = self.id).filter(data__month=datetime.now().month).filter(tipo='S')
        
        total_valor  = calcula_total(valores, 'valor')
        
        return total_valor

    def calcula_percentual_gasto_por_categoria(self):
       return int((self.total_gasto() * 100) / self.valor_planejamento)
    
    #TODO: terminar loadbar 
    def gastos(self):
        from extrato.models import mValores
        from .utils import calcula_total
        valores = mValores.objects.filter(data__month=datetime.now().month).filter(tipo='S')
        
        gastos_total  = calcula_total(valores, 'valor')

        print(f'total de:{gastos_total}')

        return 10


class mConta(models.Model):
    banco_choices = (
        ('NU', 'Nubank'),
        ('CE', 'Caixa economica')
    )

    tipo_choices = (
        ('pf', 'Pessoa fisica'),
        ('pj', 'Pessoa juridica'),
    )

    apelido = models.CharField(max_length=50)
    banco = models.CharField(max_length=2, choices=banco_choices)
    tipo = models.CharField(max_length=2, choices=tipo_choices)
    valor = models.FloatField(default=0)
    icone = models.ImageField(upload_to="icones")

    def __str__(self):
        return self.apelido
    
    