from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Count
from categoria.models import Categoria
from produtos.models import Produto
from home.models import CarouselSlide  # Adicionar importação do modelo CarouselSlide

def visualizarHome(request):
    produtos = Produto.objects.all().filter(esta_disponivel=True)
    categorias = Categoria.objects.annotate(
        produto_count=Count('produto')
    ).all()
    
    # Adicionar os slides do carrossel ao contexto
    carousel_slides = CarouselSlide.objects.filter(active=True).order_by('order')
    
    # Combine produtos, categorias e slides em um único context
    context = {
        'produtos': produtos,
        'categorias': categorias,
        'carousel_slides': carousel_slides  # Adicionar os slides ao contexto
    }

    return render(request, 'home.html', context)