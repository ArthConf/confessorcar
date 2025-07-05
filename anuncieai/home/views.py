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

# home/views.py
import base64
import os
import uuid
from django.core.files.base import ContentFile

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
    
    # Verificar se o formulário é válido
    if form.is_valid():
        slide = form.save(commit=False)
        
        # Processar a imagem cortada se foi enviada
        cropped_image_data = request.POST.get('cropped_image_data')
        if cropped_image_data and cropped_image_data.startswith('data:image'):
            # Extrair os dados da imagem do formato base64
            format, imgstr = cropped_image_data.split(';base64,')
            ext = format.split('/')[-1]
            
            # Gerar um nome de arquivo único
            filename = f"{uuid.uuid4()}.{ext}"
            
            # Converter os dados base64 em um arquivo
            image_data = ContentFile(base64.b64decode(imgstr), name=filename)
            
            # Atribuir ao campo de imagem do slide
            slide.image = image_data
        
        # Salvar o slide
        slide.save()
        messages.success(request, "Slide salvo com sucesso!")
    else:
        errors = []
        for field, error_list in form.errors.items():
            for error in error_list:
                errors.append(f"{field}: {error}")
        error_message = ", ".join(errors)
        messages.error(request, f"Erro ao salvar o slide: {error_message}")
    
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