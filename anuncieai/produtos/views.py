from django.shortcuts import get_object_or_404, render
from categoria.models import Categoria
from produtos.models import Produto

def visualizarLoja(request, categoria_slug=None):
    categorias = Categoria.objects.all()  # Pega todas as categorias para o menu
    produtos = None
    categoria_atual = None

    if categoria_slug:
        # Se uma categoria foi selecionada
        categoria_atual = get_object_or_404(Categoria, slug=categoria_slug)
        produtos = Produto.objects.filter(categoria=categoria_atual, esta_disponivel=True)
    else:
        # Se nenhuma categoria foi selecionada, mostra todos os produtos
        produtos = Produto.objects.filter(esta_disponivel=True)

    produtos_quant = produtos.count()

    # Print para debug
    print(f"Categoria selecionada: {categoria_atual}")
    print(f"Quantidade de produtos: {produtos_quant}")
    print(f"Produtos encontrados: {[p.produto_nome for p in produtos]}")

    context = {
        'produtos': produtos,
        'produtos_quant': produtos_quant,
        'categorias': categorias,  # Para mostrar o menu de categorias
        'categoria_atual': categoria_atual,  # Para destacar a categoria selecionada
    }

    return render(request, 'loja/loja.html', context)

def produto_detalhe(request, categoria_slug, produto_slug):
    try:
        produto = Produto.objects.get(categoria__slug=categoria_slug, slug=produto_slug)
    except Exception as e:
        raise e

    context = {
        'produto': produto,
    }

    return render(request, 'loja/produto_detalhe.html', context)  # Adicionei o context aqui