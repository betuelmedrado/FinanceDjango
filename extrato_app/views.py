from django.shortcuts import render, HttpResponse, redirect
from django.http import FileResponse     # aqui também tem o HttpResponse
from perfil.models import Categoria, Conta
from .models import Valores
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime
from django.template.loader import render_to_string

# para gerar o pdf
import os
from django.conf import settings
from weasyprint import HTML
from io import BytesIO

# Create your views here.


def novo_valor(request):

    if request.method == 'GET':
        conta = Conta.objects.all()
        categoria = Categoria.objects.all()

        return render(request, 'novo_valor.html', {'conta':conta, 'categoria':categoria})

    elif request.method == 'POST':

        valor = request.POST.get('valor')
        categoria = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        data = request.POST.get('data')
        conta = request.POST.get('conta')
        tipo = request.POST.get('tipo')

        db_valores = Valores(
            valor=valor,
            categoria_id=categoria,
            descricao=descricao,
            data=data,
            conta_id=conta,
            tipo=tipo,
        )
        db_valores.save()

        conta = Conta.objects.get(id=conta)

        if tipo == 'E':
            conta.valor += int(valor)
        else:
            conta.valor -= int(valor)

        conta.save()
        messages.add_message(request, constants.SUCCESS, 'Entrada/Saida Cadastrada com sucesso!')
        return redirect('/extrato/novo_valor')


def view_extrato(request):

    conta = Conta.objects.all()
    categoria = Categoria.objects.all()

    conta_get = request.GET.get('conta')
    categoria_get = request.GET.get('categoria')

    # pega as conta do mês actual "datetime.now().month
    valor = Valores.objects.filter(data__month=datetime.now().month)

    if conta_get:
        # como já foi filtrada logo a cima eu faço mais um filtro com o impressionar do botão no html
        valor = Valores.objects.filter(conta_id=conta_get)
        print(conta_get)
    if categoria_get:
        valor = Valores.objects.filter(categoria_id=categoria_get)

    return render(request, 'view_extrato.html', {'valores': valor, 'contas': conta, 'categorias': categoria})


def exportar_pdf(request):
    valor = Valores.objects.filter(data__month=datetime.now().month)

    # para buscar o caminho do arquivo extrato/ foi importado o "os" e "settings"
    path_template = os.path.join(settings.BASE_DIR, 'templates/partials/extrato.html')
    template_render = render_to_string(path_template, {'valores':valor})

    # para salvar o pdf em memoria ram  não em um path
    path_output = BytesIO()

    HTML(string=template_render).write_pdf(path_output)

    # aqui é para voltar o ponteiro do arquivo para o inicio, como funciona os arquivos
    # "seek" é para mecher no ponteiro
    path_output.seek(0)

    return FileResponse(path_output, filename='extrato.pdf')

def limpar_field_filter(request):

    # request.GET.get('conta')
    # request.GET.get('categoria')

    # print('conta ',conta)

    return redirect(request)