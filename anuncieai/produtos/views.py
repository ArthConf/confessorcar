import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from categoria.models import Categoria
from produtos.models import Produto, ProdutoImagem
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProdutoForm, ProdutoImagemForm
from django.db.models import Prefetch
from .models import Cidade

def get_cidades(request):
    """
    View para retornar cidades baseadas no estado selecionado
    """
    estado = request.GET.get('estado', '')
    if not estado:
        return JsonResponse({'cidades': []})
    
    # Buscar cidades do estado ordenadas por nome
    cidades = Cidade.objects.filter(estado=estado).order_by('nome')
    
    # Formatar para JSON
    cidades_json = [{'id': cidade.id, 'nome': cidade.nome} for cidade in cidades]
    
    return JsonResponse({'cidades': cidades_json})

def visualizarLoja(request, categoria_slug=None):
    """
    View para visualização da loja com filtros e busca.
    """
    # Inicialização da consulta base
    produtos_query = Produto.objects.filter(esta_disponivel=True).prefetch_related(
        Prefetch('imagens_produto', queryset=ProdutoImagem.objects.order_by('ordem'))
    )
    
    # Inicialização de variáveis para o contexto
    categorias = Categoria.objects.all()
    categoria_atual = None
    categorias_selecionadas = []
    
    # Filtro por categoria específica via slug da URL
    if categoria_slug:
        categoria_atual = get_object_or_404(Categoria, slug=categoria_slug)
        produtos_query = produtos_query.filter(categoria=categoria_atual)
    
    # Processar categorias selecionadas via checkbox múltiplo
    categorias_ids = request.GET.getlist('categorias')
    if categorias_ids:
        categorias_selecionadas = categorias_ids
        produtos_query = produtos_query.filter(categoria_id__in=categorias_ids)
    
    # Busca por termo (marca, modelo ou nome do produto)
    search = request.GET.get('search', '')
    if search:
        from django.db.models import Q
        produtos_query = produtos_query.filter(
            Q(produto_nome__icontains=search) | 
            Q(marca__icontains=search) | 
            Q(descricao__icontains=search)
        )
    
    # Filtro por marca
    marca = request.GET.get('marca')
    if marca:
        produtos_query = produtos_query.filter(marca=marca)
    
    # Filtro por cor
    cor = request.GET.get('cor')
    if cor:
        produtos_query = produtos_query.filter(cor=cor)
    
    # Filtro por faixa de preço
    preco_min = request.GET.get('preco_min')
    if preco_min:
        try:
            produtos_query = produtos_query.filter(preco__gte=float(preco_min))
        except (ValueError, TypeError):
            pass
    
    preco_max = request.GET.get('preco_max')
    if preco_max:
        try:
            produtos_query = produtos_query.filter(preco__lte=float(preco_max))
        except (ValueError, TypeError):
            pass
    
    # Filtro por ano
    ano_min = request.GET.get('ano_min')
    if ano_min:
        try:
            produtos_query = produtos_query.filter(ano_fabricacao__gte=int(ano_min))
        except (ValueError, TypeError):
            pass
    
    ano_max = request.GET.get('ano_max')
    if ano_max:
        try:
            produtos_query = produtos_query.filter(ano_fabricacao__lte=int(ano_max))
        except (ValueError, TypeError):
            pass
    
    # Ordenação
    sort = request.GET.get('sort', 'recentes')
    if sort == 'preco-asc':
        produtos_query = produtos_query.order_by('preco')
    elif sort == 'preco-desc':
        produtos_query = produtos_query.order_by('-preco')
    elif sort == 'ano-desc':
        produtos_query = produtos_query.order_by('-ano_fabricacao')
    elif sort == 'ano-asc':
        produtos_query = produtos_query.order_by('ano_fabricacao')
    else:  # recentes (padrão)
        produtos_query = produtos_query.order_by('-criado_em')
    
    # Dados para filtros
    from django.db.models import Count
    
    # Contar produtos por categoria
    categorias_com_contagem = Categoria.objects.annotate(produto_count=Count('produto'))
    
    # Obter marcas únicas e contagem
    marcas_data = []
    marcas_unicas = Produto.objects.filter(esta_disponivel=True).values_list('marca', flat=True).distinct()
    
    for m in marcas_unicas:
        if m:  # Evitar marcas vazias
            count = Produto.objects.filter(esta_disponivel=True, marca=m).count()
            marcas_data.append({
                'nome': m,
                'count': count
            })
    
    # Lista de anos para o filtro
    import datetime
    current_year = datetime.datetime.now().year
    anos = list(range(current_year, current_year - 30, -1))
    
    # Lista de cores completa (definida manualmente)
    COR_CHOICES = [
        ('preto', 'Preto'),
        ('branco', 'Branco'),
        ('prata', 'Prata'),
        ('cinza', 'Cinza'),
        ('vermelho', 'Vermelho'),
        ('azul', 'Azul'),
        ('azul_marinho', 'Azul Marinho'),
        ('azul_claro', 'Azul Claro'),
        ('verde', 'Verde'),
        ('verde_escuro', 'Verde Escuro'),
        ('verde_militar', 'Verde Militar'),
        ('amarelo', 'Amarelo'),
        ('laranja', 'Laranja'),
        ('marrom', 'Marrom'),
        ('bege', 'Bege'),
        ('dourado', 'Dourado'),
        ('grafite', 'Grafite'),
        ('vinho', 'Vinho'),
        ('bordô', 'Bordô'),
        ('bronze', 'Bronze'),
        ('chumbo', 'Chumbo'),
        ('champagne', 'Champagne'),
        ('rosa', 'Rosa'),
        ('roxo', 'Roxo'),
        ('violeta', 'Violeta'),
        ('cinza_escuro', 'Cinza Escuro'),
        ('cinza_claro', 'Cinza Claro'),
        ('marfim', 'Marfim'),
        ('titanium', 'Titanium'),
        ('prata_fosco', 'Prata Fosco'),
        ('preto_fosco', 'Preto Fosco'),
    ]
    
    # Cores disponíveis com os hexadecimais correspondentes
    cores_mapeamento = {
        'preto': '#000000',
        'branco': '#FFFFFF',
        'prata': '#C0C0C0',
        'cinza': '#808080',
        'cinza_escuro': '#404040',
        'cinza_claro': '#D3D3D3',
        'vermelho': '#FF0000',
        'azul': '#0066CC',
        'azul_marinho': '#000080',
        'azul_claro': '#87CEEB',
        'verde': '#008000',
        'verde_escuro': '#006400',
        'verde_militar': '#556B2F',
        'amarelo': '#FFFF00',
        'laranja': '#FFA500',
        'marrom': '#8B4513',
        'bege': '#F5F5DC',
        'dourado': '#FFD700',
        'grafite': '#696969',
        'vinho': '#800000',
        'bordô': '#800020',
        'bronze': '#CD7F32',
        'chumbo': '#708090',
        'champagne': '#F7E7CE',
        'rosa': '#FFC0CB',
        'roxo': '#800080',
        'violeta': '#EE82EE',
        'marfim': '#FFFFF0',
        'titanium': '#878681',
        'prata_fosco': '#A9A9A9',
        'preto_fosco': '#1A1A1A',
    }
    
    # Lista formatada de cores para o template
    cores_lista = []
    
    # Adicionar apenas as cores que têm veículos
    for cor_value, cor_label in COR_CHOICES:
        count = produtos_query.filter(cor=cor_value).count()
        if count > 0:  # Incluir apenas as cores que têm veículos
            hex_color = cores_mapeamento.get(cor_value, '#000000')  # Valor padrão preto se não encontrar
            cores_lista.append({
                'valor': cor_value,
                'label': cor_label,
                'hex': hex_color,
                'count': count
            })
    
    # Paginação
    from django.core.paginator import Paginator
    paginator = Paginator(produtos_query, 12)  # 12 produtos por página
    page_number = request.GET.get('page', 1)
    produtos_paginados = paginator.get_page(page_number)
    
    # Total de produtos disponíveis
    produtos_total = Produto.objects.filter(esta_disponivel=True).count()
    
    # Contexto a ser passado para o template
    context = {
        'produtos': produtos_paginados,
        'produtos_quant': produtos_query.count(),
        'produtos_total': produtos_total,
        'categorias': categorias_com_contagem,
        'categoria_atual': categoria_atual,
        'marcas': marcas_data,  # Lista de dicionários com nome e contagem
        'anos': anos,
        'cores': cores_lista,   # Lista de dicionários com informações das cores
        'search_query': search,
        'categorias_selecionadas': categorias_selecionadas,  # Lista de IDs de categorias selecionadas
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
    # Se o usuário é staff ou superuser, mostrar todos os produtos
    if request.user.is_staff or request.user.is_superuser:
        produtos = Produto.objects.all().prefetch_related(
            Prefetch('imagens_produto', queryset=ProdutoImagem.objects.order_by('ordem'))
        ).order_by('-criado_em')
    else:
        # Caso contrário, mostrar apenas os produtos do usuário logado
        produtos = Produto.objects.filter(user=request.user).prefetch_related(
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
                # Salvar produto, mas ainda não persistir no banco
                produto = form.save(commit=False)
                
                # Associar o usuário logado ao produto
                produto.user = request.user
                
                # Processa o campo cidade_texto para encontrar ou criar um objeto Cidade
                cidade_nome = form.cleaned_data.get('cidade_texto')
                estado = form.cleaned_data.get('estado')
                
                if cidade_nome and estado:
                    # Tenta encontrar a cidade, se não existir, cria
                    cidade, created = Cidade.objects.get_or_create(
                        nome=cidade_nome, 
                        estado=estado
                    )
                    produto.cidade = cidade  # Associa a cidade ao produto
                    print(f"Cidade associada: {cidade.nome}/{cidade.estado} (ID: {cidade.id}, Created: {created})")
                else:
                    print("Sem cidade ou estado para associar")
                
                # Agora sim, salvar o produto com o usuário associado
                produto.save()
                
                print(f"Produto salvo com ID: {produto.id}, Nome: {produto.produto_nome}")
                
                # Processar múltiplas imagens
                imagens = request.FILES.getlist('imagens')
                print(f"Imagens para processar: {len(imagens)}")
                
                # Verificar se existe um campo imagem_capa para definir qual será a capa
                imagem_capa_index = None
                if 'imagem_capa' in request.POST:
                    try:
                        imagem_capa_index = int(request.POST['imagem_capa'])
                        print(f"Imagem definida como capa: índice {imagem_capa_index}")
                    except (ValueError, TypeError) as e:
                        print(f"Erro ao processar índice da imagem capa: {e}")
                        imagem_capa_index = None
                
                # Processar e salvar as imagens
                for i, imagem in enumerate(imagens[:12]):  # Limita a 12 imagens
                    try:
                        # Definir ordem: 0 para a capa, valores crescentes para as demais
                        ordem = 0 if i == imagem_capa_index else i + 1
                        
                        img = ProdutoImagem.objects.create(
                            produto=produto,
                            imagem=imagem,
                            ordem=ordem
                        )
                        print(f"Imagem {i+1} salva com ID: {img.id}, Ordem: {ordem}")
                    except Exception as e:
                        print(f"Erro ao salvar imagem {i+1}: {e}")
                
                # Log para verificar a ordem das imagens após o salvamento
                imagens_salvas = ProdutoImagem.objects.filter(produto=produto).order_by('ordem')
                ordem_log = {img.id: img.ordem for img in imagens_salvas}
                print(f"Ordem das imagens após salvamento: {ordem_log}")
                
                # Verificar qual imagem é a capa (ordem=0)
                capa = imagens_salvas.filter(ordem=0).first()
                if capa:
                    print(f"Imagem de capa: ID={capa.id}, Ordem={capa.ordem}")
                else:
                    print("Nenhuma imagem com ordem=0 encontrada. Definindo a primeira como capa.")
                    # Se nenhuma imagem foi definida como capa, definir a primeira como capa
                    primeira_imagem = imagens_salvas.first()
                    if primeira_imagem:
                        primeira_imagem.ordem = 0
                        primeira_imagem.save()
                        
                        # Ajustar ordens das demais imagens
                        outras_imagens = imagens_salvas.exclude(id=primeira_imagem.id)
                        for i, img in enumerate(outras_imagens):
                            img.ordem = i + 1
                            img.save()
                
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
    
    categorias = Categoria.objects.all().order_by('categoria_nome')

    return render(request, 'produtos/form_produto.html', {
        'form': form,
        'title': 'Adicionar Produto',
        'OPCIONAIS_CONFORTO': Produto.OPCIONAIS_CONFORTO,
        'OPCIONAIS_SEGURANCA': Produto.OPCIONAIS_SEGURANCA,
        'OPCIONAIS_TECNOLOGIA': Produto.OPCIONAIS_TECNOLOGIA,
        'OPCIONAIS_OUTROS': Produto.OPCIONAIS_OUTROS,
        'categorias': categorias,  # Adicionar ao contexto
    })

@login_required
def editar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            # Salvar produto, mas não comitar ainda para processar as imagens
            produto = form.save(commit=False)
            
            # Processa o campo cidade_texto para encontrar ou criar um objeto Cidade
            cidade_nome = form.cleaned_data.get('cidade_texto')
            estado = form.cleaned_data.get('estado')
            
            if cidade_nome and estado:
                # Tenta encontrar a cidade, se não existir, cria
                cidade, created = Cidade.objects.get_or_create(
                    nome=cidade_nome, 
                    estado=estado
                )
                produto.cidade = cidade  # Associa a cidade ao produto
                print(f"Cidade associada ao editar: {cidade.nome}/{cidade.estado} (ID: {cidade.id})")
            else:
                # Se o usuário removeu a cidade ou o estado, remova a referência
                produto.cidade = None
                print("Removida associação de cidade")
            
           
            # Processar quais imagens serão mantidas/removidas
            imagens_a_manter = []
            imagens_a_remover = []
            
            # Verificar todas as imagens existentes
            for imagem in produto.imagens_produto.all():
                # Verificar se o checkbox para manter esta imagem está marcado
                if f'manter_imagem_{imagem.id}' in request.POST:
                    imagens_a_manter.append(imagem)
                else:
                    imagens_a_remover.append(imagem)
            
            # Log para debug
            print(f"Imagens a manter: {len(imagens_a_manter)}")
            print(f"Imagens a remover: {len(imagens_a_remover)}")
            
            # Remover as imagens desmarcadas
            for imagem in imagens_a_remover:
                print(f"Removendo imagem ID: {imagem.id}")
                imagem.delete()
            
            # Agora podemos salvar o produto
            produto.save()
            
            # Processar a ordem das imagens que foram mantidas
            if 'imagens_ordem' in request.POST and request.POST['imagens_ordem']:
                try:
                    ordens = json.loads(request.POST['imagens_ordem'])
                    print(f"Processando ordem das imagens: {ordens}")
                    
                    # Verificar se há alguma imagem com ordem=0 (capa)
                    tem_capa = False
                    for imagem_id_str, ordem in ordens.items():
                        if int(ordem) == 0:
                            tem_capa = True
                            break
                    
                    # Se não houver imagem com ordem=0 e tivermos imagens mantidas, definir a primeira como capa
                    imagens_atuais = list(produto.imagens_produto.all())
                    if not tem_capa and imagens_atuais:
                        primeira_imagem = imagens_atuais[0]
                        primeira_id = str(primeira_imagem.id)
                        if primeira_id in ordens:
                            ordens[primeira_id] = 0
                        else:
                            # Se a primeira imagem não está no dicionário de ordens, adicioná-la
                            ordens[primeira_id] = 0
                    
                    # Processar e salvar as ordens das imagens restantes
                    for imagem_id_str, ordem in ordens.items():
                        try:
                            imagem_id = int(imagem_id_str)
                            imagem = ProdutoImagem.objects.filter(id=imagem_id, produto=produto).first()
                            if imagem:
                                imagem.ordem = int(ordem)
                                imagem.save()
                                print(f"Ordem da imagem {imagem_id} atualizada para {ordem}")
                        except (ValueError, TypeError) as e:
                            print(f"Erro ao processar imagem ID {imagem_id_str}: {e}")
                except json.JSONDecodeError as e:
                    print(f"Erro ao decodificar JSON de ordem de imagens: {e}")
            
            # Processar múltiplas imagens novas
            imagens = request.FILES.getlist('imagens')
            if imagens:
                print(f"Processando {len(imagens)} novas imagens")
                
                # Determinar a próxima ordem disponível
                from django.db.models import Max
                max_ordem = produto.imagens_produto.aggregate(Max('ordem'))['ordem__max'] or -1
                if max_ordem < 0:  # Se não houver imagens existentes
                    max_ordem = -1  # Começará do 0
                
                # Verificar se alguma nova imagem deve ser a capa
                imagem_capa_index = None
                if 'imagem_capa' in request.POST:
                    try:
                        imagem_capa_index = int(request.POST['imagem_capa'])
                        print(f"Nova imagem de capa: índice {imagem_capa_index}")
                    except (ValueError, TypeError) as e:
                        print(f"Erro ao processar índice da nova imagem capa: {e}")
                        imagem_capa_index = None
                
                # Adicionar as novas imagens
                for i, imagem in enumerate(imagens[:12]):
                    try:
                        # Determinar a ordem da imagem
                        # Se há um índice específico para capa e este é ele, usar ordem=0
                        # Se não há imagens existentes e esta é a primeira, usar ordem=0
                        # Caso contrário, incrementar a partir da última ordem existente
                        if i == imagem_capa_index:
                            ordem = 0
                        elif max_ordem == -1 and i == 0 and not produto.imagens_produto.exists():
                            ordem = 0
                        else:
                            ordem = max_ordem + i + 1
                        
                        # Criar o objeto de imagem
                        img = ProdutoImagem.objects.create(
                            produto=produto,
                            imagem=imagem,
                            ordem=ordem
                        )
                        print(f"Nova imagem adicionada: ID={img.id}, Ordem={ordem}")
                        
                        # Se esta imagem é a capa, atualizar as demais imagens para não serem capa
                        if ordem == 0:
                            # Buscar outras imagens com ordem=0 e atualizá-las
                            imagens_antigas_capa = produto.imagens_produto.filter(ordem=0).exclude(id=img.id)
                            for idx, img_antiga in enumerate(imagens_antigas_capa):
                                nova_ordem = max_ordem + len(imagens) + idx + 1
                                img_antiga.ordem = nova_ordem
                                img_antiga.save()
                                print(f"Antiga imagem capa atualizada: ID={img_antiga.id}, Nova Ordem={nova_ordem}")
                    except Exception as e:
                        print(f"Erro ao salvar nova imagem {i+1}: {e}")
            
            messages.success(request, f'Produto "{produto.produto_nome}" atualizado com sucesso!')
            return redirect('produtos:gerenciar_produtos')
        else:
            print("Formulário inválido:", form.errors)
            for field, errors in form.errors.items():
                print(f"Campo {field}: {errors}")
    else:
        form = ProdutoForm(instance=produto)
        
    categorias = Categoria.objects.all().order_by('categoria_nome')
    return render(request, 'produtos/form_produto.html', {
        'form': form,
        'produto': produto,
        'title': 'Editar Produto',
        'OPCIONAIS_CONFORTO': Produto.OPCIONAIS_CONFORTO,
        'OPCIONAIS_SEGURANCA': Produto.OPCIONAIS_SEGURANCA,
        'OPCIONAIS_TECNOLOGIA': Produto.OPCIONAIS_TECNOLOGIA,
        'OPCIONAIS_OUTROS': Produto.OPCIONAIS_OUTROS,
        'imagens_atuais': produto.imagens_produto.all().order_by('ordem'),
        'categorias': categorias,
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
    """View para remover uma imagem específica"""
    if request.method == 'POST':
        try:
            produto = get_object_or_404(Produto, pk=produto_pk)
            imagem = get_object_or_404(ProdutoImagem, pk=imagem_pk, produto=produto)
            
            # Verificar se a imagem é a capa (ordem=0)
            era_capa = imagem.ordem == 0
            
            # Excluir a imagem
            imagem.delete()
            
            # Se a imagem excluída era a capa, definir uma nova capa
            if era_capa:
                # Pegar a primeira imagem disponível e definir como capa (ordem=0)
                nova_capa = ProdutoImagem.objects.filter(produto=produto).first()
                if nova_capa:
                    nova_capa.ordem = 0
                    nova_capa.save()
            
            # Reordenar as imagens restantes
            imagens_restantes = ProdutoImagem.objects.filter(produto=produto).exclude(ordem=0).order_by('ordem')
            for i, img in enumerate(imagens_restantes, 1):
                img.ordem = i
                img.save()
            
            # Se for uma solicitação AJAX, retornar JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success', 
                    'message': 'Imagem removida com sucesso!',
                    'imagens_restantes': list(produto.imagens_produto.values('id', 'ordem'))
                })
                
            messages.success(request, 'Imagem removida com sucesso!')
            return redirect('produtos:editar_produto', pk=produto_pk)
            
        except Exception as e:
            print(f"Erro ao remover imagem: {e}")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
                
            messages.error(request, f'Erro ao remover imagem: {str(e)}')
            return redirect('produtos:editar_produto', pk=produto_pk)
            
    # Se não for POST, redirecionar para gerenciamento de produtos
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