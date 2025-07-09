import os
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .forms import LoginForm, RegisterForm
import logging
# users/views.py
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import ProfileEditForm
from localflavor.br.br_states import STATE_CHOICES
@login_required
def edit_profile_view(request):
    """
    View para edição de perfil do usuário
    """
    # Lista de estados para o formulário
    estados = STATE_CHOICES
    
    if request.method == 'POST':
        # Atualizar dados do usuário
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        
        # Atualizar dados do perfil
        profile = request.user.profile
        profile.whatsapp = request.POST.get('whatsapp', '')
        profile.cpf = request.POST.get('cpf', '')
        profile.endereco = request.POST.get('endereco', '')
        profile.bairro = request.POST.get('bairro', '')
        profile.cidade = request.POST.get('cidade', '')
        profile.estado = request.POST.get('estado', '')
        profile.cep = request.POST.get('cep', '')
        
        # Processar avatar
        if 'avatar' in request.FILES:
            # Excluir avatar antigo se existir
            if profile.avatar:
                try:
                    if os.path.isfile(profile.avatar.path):
                        os.remove(profile.avatar.path)
                except Exception as e:
                    print(f"Erro ao excluir avatar: {e}")
            
            profile.avatar = request.FILES['avatar']
        
        profile.save()
        
        messages.success(request, "Perfil atualizado com sucesso!")
        return redirect('users:dashboard')
    
    context = {
        'estados': estados,
        'user': request.user,
    }
    
    return render(request, 'users/edit_profile.html', context)

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Mantém o usuário logado após a mudança de senha
            messages.success(request, 'Sua senha foi alterada com sucesso!')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    return redirect('users:dashboard')
# Configure o logger
logger = logging.getLogger(__name__)

def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, 'Você já está logado.')
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo de volta, {username}!')
                
                # Redireciona para a página que o usuário tentou acessar
                next_page = request.GET.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect('home')
            else:
                messages.error(request, 'Nome de usuário ou senha incorretos.')
    else:
        form = LoginForm()
    
    return render(request, 'users/login.html', {'form': form})

@transaction.atomic
def register_view(request):
    if request.user.is_authenticated:
        logger.info('Usuário já autenticado tentando acessar o registro')
        messages.info(request, 'Você já está registrado e logado.')
        return redirect('home')

    if request.method == 'POST':
        logger.info('Recebido POST para registro de usuário')
        form = RegisterForm(request.POST)
        
        # Log dos dados recebidos (omitindo senha por segurança)
        post_data = {k: v for k, v in request.POST.items() if 'password' not in k}
        logger.info(f'Dados do formulário: {post_data}')
        
        try:
            if form.is_valid():
                logger.info('Formulário válido, salvando usuário')
                user = form.save()
                login(request, user)
                messages.success(request, 'Sua conta foi criada com sucesso! Bem-vindo!')
                logger.info(f'Usuário {user.username} registrado com sucesso')
                return redirect('home')
            else:
                logger.warning(f'Erros no formulário: {form.errors}')
                for field, errors in form.errors.items():
                    logger.warning(f'Campo {field}: {errors}')
                messages.error(request, 'Por favor, corrija os erros abaixo.')
        except Exception as e:
            logger.error(f'Erro ao registrar usuário: {str(e)}', exc_info=True)
            messages.error(request, f'Ocorreu um erro ao processar seu cadastro: {str(e)}')
    else:
        logger.info('Carregando formulário de registro vazio')
        form = RegisterForm()
    
    return render(request, 'users/register.html', {'form': form})

def logout_view(request):
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        messages.success(request, f'Até logo, {username}!')
    return redirect('home')

@login_required
def dashboard_view(request):
    context = {
        'user': request.user
    }
    return render(request, 'users/dashboard.html', context)