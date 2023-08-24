from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Conta, Categoria
from extrato_app.models import Valores
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime
import utils
from contas_app.models import ContasPagar

# Para fazer a soma usando "aggregate"
from django.db.models import Sum

# Create your views here.

def home(request):

    # # geting the late bills and close to expiration
    # # pegando contas atrasadas e perto do vencimento
    # contas_vencidas = ver_contas(request)

    conta = Conta.objects.all()
    total = utils.calcular_total(conta,'valor')

    # == Here olny to get the spend essecial and not essecial ==========================*
    categorias = Categoria.objects.all()
    obj_valores = Valores.objects.all()

    # filter the obj to bring only the essencial e not essencial
    percentual_essencial = utils.equilibrio_financeiro(obj_valores, 1, categorias)
    percentual_nao_essencial = utils.equilibrio_financeiro(obj_valores, 0, categorias)

    # ===================================================================================*

    conta_entrada = obj_valores.filter(data__month=datetime.now().month).filter(tipo='E')
    valor_entrada = utils.calcular_total(conta_entrada, 'valor')

    conta_saida = obj_valores.filter(data__month=datetime.now().month).filter(tipo='S')
    valor_saida = utils.calcular_total(conta_saida, 'valor')

    quantidade_vencidas = proxima_vencimento_e_vencidas(request, 'vencida')
    quantidade_a_vencer = proxima_vencimento_e_vencidas(request, 'proxima')

    print('vencida ',quantidade_vencidas)
    print(quantidade_a_vencer)
    return render(request,'home.html', {'valor_total':total, 'conta':conta, 'percentual_essencial':int(percentual_essencial), 'percentual_nao_essencial':int(percentual_nao_essencial),
                                        'valor_entrada': valor_entrada, 'valor_saida':valor_saida, 'quantidade_vencidas': quantidade_vencidas, 'quantidade_a_vencer':quantidade_a_vencer})

def proxima_vencimento_e_vencidas(request, argumento):

    dia_atual = datetime.now().day

    contas = ''
    quantidade = 0

    if argumento == 'vencida':
        contas = ContasPagar.objects.filter(dia_pagamento__lt=dia_atual)
    elif argumento == 'proxima':
        contas = ContasPagar.objects.exclude(dia_pagamento__lt=dia_atual).filter(dia_pagamento__lte=dia_atual + 5)

    for conta in contas:
        quantidade += 1

    return quantidade


def gerenciar(request):

    contas = Conta.objects.all()
    total_conta = 0

    # somar os valores posso fazer assin ou
    # for conta in contas:
    #     total_conta += conta.valor

    # Ou assim  Importa o aggregate primeiro
    total_conta = contas.aggregate(Sum('valor'))['valor__sum']

    categoria = Categoria.objects.all()

    return render(request, 'gerenciar.html', {'conta':contas, 'total_conta':total_conta, 'categoria':categoria})


def cadastrar_banco(request):

    # Pegando o request do usuario
    apelido = request.POST.get('apelido')
    banco = request.POST.get('banco')
    tipo = request.POST.get('tipo')
    valor = request.POST.get('valor')
    icone = request.FILES.get('icone')

    if len(apelido.strip()) == 0 or len(valor.strip()) == 0:

        messages.add_message(request, constants.ERROR, 'Preencha todos campos!')
        return redirect('/perfil/home/gerenciar')
        # mensagem de erro

    conta = Conta(
        apelido = apelido,
        banco = banco,
        tipo = tipo,
        valor = valor,
        icon = icone
    )

    conta.save()
    messages.add_message(request, constants.SUCCESS, 'Conta cadastrado com sucesso')
    return redirect('/perfil/home/gerenciar')


def deletar_banco(request, id):

    conta = Conta.objects.get(id=id)
    conta.delete()

    messages.add_message(request, constants.SUCCESS, 'Conta deletada com sucesso!')
    return redirect('/perfil/home/gerenciar')


def cadastrar_categoria(request):

    categoria = request.POST.get('categoria')
    essencial = bool(request.POST.get('essencial'))

    if len(categoria.strip()) == 0:
        messages.add_message(request, constants.ERROR, ' Preencha o campo categoria!')


    data_base = Categoria(
        categoria = categoria,
        essencial = essencial
    )

    data_base.save()

    messages.add_message(request, constants.SUCCESS, 'Categoria criada com sucesso!')

    return redirect('/perfil/home/gerenciar')

def update_categoria(request, id):

    categoria = Categoria.objects.get(id=id)

    categoria.essencial = not categoria.essencial

    categoria.save()

    return redirect('/perfil/home/gerenciar')


def dashboard(request):
    dados = {}
    categorias = Categoria.objects.all()

    for categoria in categorias:
        total = 0
        valores = Valores.objects.filter(categoria=categoria)
        for valor in valores:
            total += valor.valor

        dados[categoria.categoria] = total

    return render(request,'dashboard.html',{'label':list(dados.keys()),'valores':list(dados.values())})