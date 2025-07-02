from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Categoria
from .forms import CategoriaForm

@login_required
def gerenciar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'categoria/gerenciar_categorias.html', {
        'categorias': categorias
    })

@login_required
def adicionar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria adicionada com sucesso!')
            return redirect('categoria:gerenciar_categorias')
    else:
        form = CategoriaForm()
    
    return render(request, 'categoria/form_categoria.html', {
        'form': form,
        'title': 'Adicionar Categoria'
    })

@login_required
def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, request.FILES, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria atualizada com sucesso!')
            return redirect('categoria:gerenciar_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    
    return render(request, 'categoria/form_categoria.html', {
        'form': form,
        'title': 'Editar Categoria'
    })

@login_required
def excluir_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoria excluída com sucesso!')
        return redirect('categoria:gerenciar_categorias')
    
    return render(request, 'categoria/confirmar_exclusao.html', {
        'categoria': categoria
    })