from django.db import models
from perfil.models import mCategoria

# Create your models here.
class mContaPagar(models.Model):
    titulo = models.CharField(max_length=50)
    categoria = models.ForeignKey(mCategoria, on_delete=models.DO_NOTHING)
    descricao = models.TextField()
    valor = models.FloatField()
    dia_pagamento = models.IntegerField()

    def __str__(self):
        return self.titulo
    

class mContaPaga(models.Model):
    conta = models.ForeignKey(mContaPagar, on_delete=models.DO_NOTHING)
    data_pagamento = models.DateField()