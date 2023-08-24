
# To do the sum of aggregate
from django.db.models import Sum

def calcular_total(obj, campo):

    total = 0
    for itens in obj:
        total += getattr(itens, campo)

    return total


def equilibrio_financeiro(obj_valor, campo_essencial, obj_categoria):

    try:
        # valores_total_por_essencial = obj_categoria.filter(essencial=campo_essencial).aggregate(Sum('valor_planejamento'))['valor_planejamento__sum']

        # pegando no model categoria se é essencial ou não
        categoria_essencial = obj_categoria.filter(essencial=campo_essencial)

        # filtrando pelo categoria os valores essencial ou não
        valor_essencial = obj_valor.filter(tipo='S').filter(categoria__in=categoria_essencial).aggregate(Sum('valor'))['valor__sum']

        # usando a função "calcula_total" mais dava para usar o aggregate para somar os valores total-
            # tamto essencial quanto não essencil para porcentagem sobre o valor gasto
        valores_total_de_saida = calcular_total(obj_valor.filter(tipo='S'), 'valor')

        percentual = valor_essencial * 100 / valores_total_de_saida
    except:
        percentual = 0

    return int(percentual)
