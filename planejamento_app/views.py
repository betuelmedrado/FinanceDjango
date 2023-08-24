from django.shortcuts import render
from django.http import HttpResponse
from perfil.models import Categoria
from extrato_app.models import Valores
from django.http import HttpResponse, JsonResponse

# Aqui é para o java não prescisar capturar o crsf_token
from django.views.decorators.csrf import csrf_exempt

# para receber a requisição
import json


# Create your views here.

def definir_planejamento(request):

    categoria = Categoria.objects.all()

    return render(request, 'definir_planejamento.html', {'categorias':categoria})

@csrf_exempt
def updata_valor_categoria(request, id):

    # Recebendo os valores e carregando em formato json com "[novo_valor]" que foi enviado do frontend função javascript
    novo_valor = json.load(request)['novo_valor']
    categoria = Categoria.objects.get(id=id)

    categoria.valor_planejamento = novo_valor
    categoria.save()

    # retorna um json para o frontend
    return JsonResponse({'valor': f'Recebido  id {id}'})


def ver_planejamento(request):
    categoria = Categoria.objects.all()

    valor_total_planejamento = 0
    percentual_do_total_planejamento = 0
    for valor in categoria:
        valor_total_planejamento += valor.valor_planejamento

    # pegando o total gasto valores
    total_gasto = 0

    for total in categoria:
        total_gasto += total.total_gasto()
    try:
        percentual_do_total_planejamento += int((total_gasto * 100) / valor_total_planejamento)
    except:
        percentual_do_total_planejamento = 1

    return render(request, 'ver_planejamento.html', {'categorias':categoria, 'valor_total_planejamento': valor_total_planejamento, 'percentual_planejamento':percentual_do_total_planejamento, 'total_do_total_gasto': total_gasto})







