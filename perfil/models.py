from django.db import models
from datetime import datetime

# Create your models here.

class Categoria(models.Model):

    categoria = models.CharField(max_length=50)
    essencial = models.BooleanField(default=False)
    valor_planejamento = models.FloatField(default=0)

    def __str__(self):
        return self.categoria

    # Pegando a soma e o valores para views html "ver_planejamento" e ver os gastos
    def total_gasto(self):
        from extrato_app.models import Valores

        # Pegando o id do valor gasto da categoria atual "que estamos" e depois filtrando o mês actual e filter para saber se é uma saida do tipo "S" "saida"
        valores = Valores.objects.filter(categoria_id=self.id).filter(data__month=datetime.now().month).filter(tipo='S')
                                                                      # aqui temque ser assin "data__manth" apesar de não estar assim no "db"
        total_valores = 0
        for valor in valores:
            total_valores += valor.valor
        return total_valores

    def calcula_percentual_gasto_por_categoria(self):
        percentual = 0
        try:
            percentual = int((self.total_gasto() * 100) / self.valor_planejamento)
        except:
            percentual = 0
        return percentual


class Conta(models.Model):
    banco_choices = (
        ('NU','Nubanck'),
        ('CE','Caixa Economica'),
        ('BR','Banco do Brasil')
    )

    tipo_choices = (
        ('pf','Pessoa Física'),
        ('pj','Pessoa Jurídica')
    )

    apelido = models.CharField(max_length=50)
    banco = models.CharField(max_length=2, choices=banco_choices)
    tipo = models.CharField(max_length=2, choices=tipo_choices)
    valor = models.FloatField(default=0)
    icon = models.ImageField(upload_to='Icones')

    def __str__(self):
        return self.apelido