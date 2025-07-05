from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from categoria.models import Categoria
from produtos.models import Produto, ProdutoImagem
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProdutoForm, ProdutoImagemForm
from django.db.models import Prefetch

def visualizarLoja(request, categoria_slug=None):
    categorias = Categoria.objects.all()
    produtos = None
    categoria_atual = None

    if categoria_slug:
        categoria_atual = get_object_or_404(Categoria, slug=categoria_slug)
        produtos = Produto.objects.filter(
            categoria=categoria_atual, 
            esta_disponivel=True
        ).prefetch_related(
            Prefetch('imagens_produto', queryset=ProdutoImagem.objects.order_by('ordem'))
        )
    else:
        produtos = Produto.objects.filter(
            esta_disponivel=True
        ).prefetch_related(
            Prefetch('imagens_produto', queryset=ProdutoImagem.objects.order_by('ordem'))
        )

    produtos_quant = produtos.count()

    context = {
        'produtos': produtos,
        'produtos_quant': produtos_quant,
        'categorias': categorias,
        'categoria_atual': categoria_atual,
    }

    return render(request, 'loja/loja.html', context)

def produto_detalhe(request, categoria_slug, produto_slug):
    try:
        produto = Produto.objects.prefetch_related(
            Prefetch('imagens_produto', queryset=ProdutoImagem.objects.order_by('ordem'))
        ).get(categoria__slug=categoria_slug, slug=produto_slug)
    except Exception as e:
        raise e

    context = {
        'produto': produto,
    }

    return render(request, 'loja/produto_detalhe.html', context)

@login_required
def gerenciar_produtos(request):
    produtos = Produto.objects.all().prefetch_related(
        Prefetch('imagens_produto', queryset=ProdutoImagem.objects.order_by('ordem'))
    ).order_by('-criado_em')
    
    return render(request, 'produtos/gerenciar_produtos.html', {
        'produtos': produtos
    })

@login_required
def adicionar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        print(f"Form data: {request.POST}")
        
        if form.is_valid():
            print("Form is valid! Cleaned data:", form.cleaned_data)
            
            try:
                produto = form.save()
                print(f"Produto salvo com ID: {produto.id}, Nome: {produto.produto_nome}")
                
                # Processar múltiplas imagens
                imagens = request.FILES.getlist('imagens')
                print(f"Imagens para processar: {len(imagens)}")
                
                for i, imagem in enumerate(imagens[:12]):  # Limita a 12 imagens
                    try:
                        img = ProdutoImagem.objects.create(
                            produto=produto,
                            imagem=imagem,
                            ordem=i
                        )
                        print(f"Imagem {i+1} salva com ID: {img.id}")
                    except Exception as e:
                        print(f"Erro ao salvar imagem {i+1}: {e}")
                
                messages.success(request, f'Produto "{produto.produto_nome}" adicionado com sucesso!')
                return redirect('produtos:gerenciar_produtos')
            except Exception as e:
                print(f"ERRO ao salvar produto: {e}")
                messages.error(request, f'Erro ao salvar produto: {e}')
        else:
            print("Form is invalid! Errors:", form.errors)
            for field, errors in form.errors.items():
                print(f"Campo {field}: {errors}")
    else:
        form = ProdutoForm()
    
    return render(request, 'produtos/form_produto.html', {
        'form': form,
        'title': 'Adicionar Produto',
        'opcionais_choices': Produto.OPCIONAIS_CHOICES,
    })

@login_required
def editar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            # O método save do formulário agora cuida do slug automaticamente
            produto = form.save()
            
            # Processar múltiplas imagens
            if request.FILES.getlist('imagens'):
                # Remover imagens antigas
                produto.imagens_produto.all().delete()
                
                # Adicionar novas imagens
                imagens = request.FILES.getlist('imagens')
                for i, imagem in enumerate(imagens[:12]):
                    ProdutoImagem.objects.create(
                        produto=produto,
                        imagem=imagem,
                        ordem=i
                    )
            
            messages.success(request, f'Produto "{produto.produto_nome}" atualizado com sucesso!')
            return redirect('produtos:gerenciar_produtos')
    else:
        form = ProdutoForm(instance=produto)
    
    return render(request, 'produtos/form_produto.html', {
        'form': form,
        'produto': produto,
        'title': 'Editar Produto',
        'opcionais_choices': Produto.OPCIONAIS_CHOICES,
        'imagens_atuais': produto.imagens_produto.all().order_by('ordem'),
    })

@login_required
def excluir_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        # Primeiro excluir as imagens
        produto.imagens_produto.all().delete()
        
        nome_produto = produto.produto_nome
        produto.delete()
        messages.success(request, f'Produto "{nome_produto}" excluído com sucesso!')
        return redirect('produtos:gerenciar_produtos')
    
    return render(request, 'produtos/confirmar_exclusao.html', {
        'produto': produto,
    })

@login_required
def remover_imagem(request, produto_pk, imagem_pk):
    """Nova view para remover uma imagem específica"""
    if request.method == 'POST':
        imagem = get_object_or_404(ProdutoImagem, pk=imagem_pk, produto_id=produto_pk)
        imagem.delete()
        messages.success(request, 'Imagem removida com sucesso!')
        return redirect('produtos:editar_produto', pk=produto_pk)
    return redirect('produtos:gerenciar_produtos')

@login_required
def reordenar_imagens(request, produto_pk):
    """Nova view para reordenar as imagens"""
    if request.method == 'POST':
        ordem = request.POST.getlist('ordem[]')
        for index, imagem_id in enumerate(ordem):
            ProdutoImagem.objects.filter(pk=imagem_id).update(ordem=index)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def marcar_produto_vendido(request, pk):
    if request.method == 'POST':
        produto = get_object_or_404(Produto, pk=pk)
        produto.esta_disponivel = False
        produto.save()
        messages.success(request, f'Veículo "{produto.produto_nome}" marcado como vendido com sucesso!')
    return redirect('produtos:gerenciar_produtos')