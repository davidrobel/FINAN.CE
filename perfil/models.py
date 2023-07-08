from django.db import models

# Create your models here.
class mCategoria(models.Model):
    categoria = models.CharField(max_length=50)
    essencial = models.BooleanField(default=False)
    valor_planejamento = models.FloatField(default=0)


    def __str__(self):
        return self.categoria
    

class mConta(models.Model):
    banco_choices = (
        ('NU', 'Nubank'),
        ('CE', 'Caixa economica'),
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
    
    