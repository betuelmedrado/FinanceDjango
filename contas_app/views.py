from django.shortcuts import render, redirect
# from django.views.decorators.csrf import csrf_exempt
from perfil.models import Categoria
from .models import ContasPagar, ContaPaga
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

    # mensagesn
from django.contrib import messages
from django.contrib.messages import constants

# Create your views here.


def definir_contas(request):

    if request.method == 'GET':
        categorias = Categoria.objects.all()

        return render(request, 'definir_contas.html', {'categorias': categorias})
    else:
        titulo = request.POST.get('titulo')
        categoria = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        dia_pagamento = request.POST.get('dia_pagamento')

        contas_pagar = ContasPagar(
            titulo=titulo,
            categoria_id=categoria,
            descricao=descricao,
            valor=valor,
            dia_pagamento=dia_pagamento

        )
        contas_pagar.save()
        messages.add_message(request, constants.SUCCESS, 'Contas cadastradas com sucesso!')
        return redirect('/contas/definir_contas')

def ver_contas(request):

    MES_ATUAL = datetime.now().month
    DIA_ATUAL = datetime.now().day



    contas_a_pagar = ContasPagar.objects.all()
    contas_paga = ContaPaga.objects.filter(data_pagamento__month=MES_ATUAL).values('conta')


    #                                                    # ' __lt ' menor que =======
    contas_vencidas = contas_a_pagar.filter(dia_pagamento__lt=DIA_ATUAL).exclude(id__in=contas_paga)

    #                                                    # ' __lte ' menor igual =======        # ' __gt 'maior que =======
    contas_proxima_vencimento = contas_a_pagar.filter(dia_pagamento__lt=DIA_ATUAL + 5).exclude(id__in=contas_paga).exclude(id__in=contas_vencidas)

    contas_restantes = contas_a_pagar.exclude(id__in=contas_paga).exclude(id__in=contas_vencidas).exclude(id__in=contas_proxima_vencimento)

    return render(request,'ver_contas.html',{'contas_restantes': contas_restantes, 'contas_vencidas': contas_vencidas,
                                             'contas_proxima_vencimento':contas_proxima_vencimento, 'quant_vencida':contas_vencidas.count(),
                                             'quant_proxima_vencimento':contas_proxima_vencimento.count(),'quant_restante':contas_a_pagar.count()})


@csrf_exempt
def pagar_conta(request, id):
    data = datetime.now()

    pagar_conta = ContaPaga(
        data_pagamento = data,
        conta_id = id)

    pagar_conta.save()
    messages.add_message(request, constants.SUCCESS,'Conta Paga Com sucesso!')
    return redirect('/contas/ver_contas')