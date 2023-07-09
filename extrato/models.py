from django.db import models
from perfil.models import mCategoria, mConta

# Create your models here.
class mValores(models.Model):
    choice_tipo = (
        ('E', 'Entrada'),
        ('S', 'Saída')
    )
    
    valor = models.FloatField()
    categoria = models.ForeignKey(mCategoria, on_delete=models.DO_NOTHING)
    descricao = models.TextField()
    data = models.DateField()
    conta = models.ForeignKey(mConta, on_delete=models.DO_NOTHING)
    tipo = models.CharField(max_length=1, choices=choice_tipo)

    def __str__(self):
        return self.descricao