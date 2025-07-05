# home/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import CarouselSlide
from .forms import CarouselSlideForm

def home(request):
    # View principal da página inicial
    carousel_slides = CarouselSlide.objects.filter(active=True).order_by('order')
    # Adicione outras consultas necessárias para categorias, produtos em destaque, etc.
    
    context = {
        'carousel_slides': carousel_slides,
        # Adicione outros contextos necessários
    }
    return render(request, 'home.html', context)

@user_passes_test(lambda u: u.is_staff)
@require_POST
def save_slide(request):
    slide_id = request.POST.get('slide_id')
    
    if slide_id:
        # Editar slide existente
        try:
            slide = CarouselSlide.objects.get(id=slide_id)
            form = CarouselSlideForm(request.POST, request.FILES, instance=slide)
        except CarouselSlide.DoesNotExist:
            messages.error(request, "Slide não encontrado!")
            return redirect('home:home')
    else:
        # Novo slide
        form = CarouselSlideForm(request.POST, request.FILES)
    
    if form.is_valid():
        form.save()
        messages.success(request, "Slide salvo com sucesso!")
    else:
        messages.error(request, f"Erro ao salvar o slide: {form.errors}")
    
    return redirect('home:home')

@user_passes_test(lambda u: u.is_staff)
@require_POST
def delete_slide(request):
    slide_id = request.POST.get('slide_id')
    
    try:
        slide = CarouselSlide.objects.get(id=slide_id)
        slide.delete()
        messages.success(request, "Slide excluído com sucesso!")
    except CarouselSlide.DoesNotExist:
        messages.error(request, "Slide não encontrado!")
    
    return redirect('home:home')