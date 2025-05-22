from django.shortcuts import render

from produtos.models import Produto
# Create your views here.

def visualizarLoja(request):
    produtos = Produto.objects.all().filter(esta_disponivel=True)

    context = {
        'produtos' : produtos
    }

    return render(request, 'loja/loja.html', context)