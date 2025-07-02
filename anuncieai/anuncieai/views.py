from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Count
from categoria.models import Categoria  # Corrigido o import
from produtos.models import Produto

def visualizarHome(request):
    produtos = Produto.objects.all().filter(esta_disponivel=True)
    categorias = Categoria.objects.annotate(
        produto_count=Count('produto')
    ).all()
    
    # Combine ambos produtos e categorias em um único context
    context = {
        'produtos': produtos,
        'categorias': categorias
    }

    return render(request, 'home.html', context)