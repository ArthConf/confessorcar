# No início do arquivo forms.py, adicione a importação:
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile
from localflavor.br.forms import BRCPFField, BRStateChoiceField
import re  # Adicione esta linha
class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu e-mail'
        })
    )
    
    username = forms.CharField(
        label='Nome de usuário',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu nome de usuário'
        })
    )
    
    first_name = forms.CharField(
        label='Nome',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu nome'
        })
    )
    
    last_name = forms.CharField(
        label='Sobrenome',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu sobrenome'
        })
    )
    
    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua senha'
        }),
        help_text='A senha deve ter pelo menos 8 caracteres.'
    )
    
    password2 = forms.CharField(
        label='Confirme a senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua senha novamente'
        })
    )
    
    # Campos adicionais para o perfil
    cpf = BRCPFField(
        label='CPF',
        widget=forms.TextInput(attrs={
            'class': 'form-control cpf-mask',
            'placeholder': '000.000.000-00'
        }),
        help_text='Formato: 000.000.000-00'
    )
    
    endereco = forms.CharField(
        label='Endereço',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rua, número, complemento'
        }),
        required=False
    )
    
    bairro = forms.CharField(
        label='Bairro',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Bairro'
        }),
        required=False
    )
    
    cep = forms.CharField(
        label='CEP',
        widget=forms.TextInput(attrs={
            'class': 'form-control cep-mask',
            'placeholder': '00000-000',
            'id': 'cep'
        }),
        required=False
    )
    
    estado = BRStateChoiceField(
        label='Estado',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'estado'
        }),
        required=False
    )
    
    cidade = forms.CharField(
        label='Cidade',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'cidade',
            'list': 'cidade-list',
            'placeholder': 'Digite ou selecione sua cidade'
        }),
        required=False
    )
    
    whatsapp = forms.CharField(
        label='WhatsApp',
        widget=forms.TextInput(attrs={
            'class': 'form-control phone-mask',
            'placeholder': '(00) 00000-0000'
        }),
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Tradução das mensagens de ajuda
        self.fields['username'].help_text = 'Necessário. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.'
        self.fields['password1'].help_text = '''
            <ul>
                <li>Sua senha não pode ser muito similar às suas outras informações pessoais.</li>
                <li>Sua senha deve conter pelo menos 8 caracteres.</li>
                <li>Sua senha não pode ser uma senha comum.</li>
                <li>Sua senha não pode ser inteiramente numérica.</li>
            </ul>
        '''

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Este e-mail já está em uso.')
        return email
        
    def clean_whatsapp(self):
        whatsapp = self.cleaned_data.get('whatsapp')
        if whatsapp:
            try:
                # Remover tudo que não for dígito e formatar
                digits = re.sub(r'\D', '', whatsapp)
                
                # Se for vazio após remover caracteres não numéricos, retorne vazio
                if not digits:
                    return ''
                    
                # Verificar se tem entre 10 e 11 dígitos (permite números com e sem o 9)
                if len(digits) < 10 or len(digits) > 11:
                    raise ValidationError('Número de WhatsApp inválido. Deve conter entre 10 e 11 dígitos.')
                
                # Se tiver 10 dígitos, adiciona o 9 depois do DDD
                if len(digits) == 10:
                    digits = digits[:2] + '9' + digits[2:]
                
                # Formatar como (00) 00000-0000
                formatted = f'({digits[:2]}) {digits[2:7]}-{digits[7:]}'
                return formatted
            except Exception as e:
                # Log do erro específico
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Erro ao processar WhatsApp '{whatsapp}': {e}")
                
                # Se o campo é opcional, retorne vazio em caso de erro
                if not self.fields['whatsapp'].required:
                    return ''
                raise ValidationError(f'Formato de WhatsApp inválido: {str(e)}')
        return whatsapp

        # Na classe RegisterForm em users/forms.py, adicione este método save():
    def save(self, commit=True):
        # Primeiro salve o usuário usando o método save do UserCreationForm
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        
        if commit:
            user.save()
            
            # Agora, salve os dados do perfil
            profile = user.profile  # O profile já foi criado pelo signal
            
            # Atribuir os valores dos campos adicionais ao perfil
            profile.cpf = self.cleaned_data.get('cpf', '')
            profile.endereco = self.cleaned_data.get('endereco', '')
            profile.bairro = self.cleaned_data.get('bairro', '')
            profile.cidade = self.cleaned_data.get('cidade', '')
            profile.estado = self.cleaned_data.get('estado', '')
            profile.cep = self.cleaned_data.get('cep', '')
            profile.whatsapp = self.cleaned_data.get('whatsapp', '')
            
            # Salvar o perfil
            profile.save()
            
        return user

# users/forms.py
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['whatsapp', 'cpf', 'endereco', 'bairro', 'cidade', 'estado', 'cep', 'avatar']
    
    def clean_whatsapp(self):
        whatsapp = self.cleaned_data.get('whatsapp')
        if whatsapp:
            # Lógica de limpeza do WhatsApp
            digits = re.sub(r'\D', '', whatsapp)
            if len(digits) < 10 or len(digits) > 11:
                raise ValidationError('Número de WhatsApp inválido')
            if len(digits) == 10:
                digits = digits[:2] + '9' + digits[2:]
            return f'({digits[:2]}) {digits[2:7]}-{digits[7:]}'
        return whatsapp

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            
            # Salvar dados do perfil
            profile = user.profile
            
            # Usar get() para campos opcionais com valor padrão vazio
            profile.cpf = self.cleaned_data.get('cpf', '')
            profile.endereco = self.cleaned_data.get('endereco', '')
            profile.bairro = self.cleaned_data.get('bairro', '')
            profile.cidade = self.cleaned_data.get('cidade', '')
            profile.estado = self.cleaned_data.get('estado', '')
            profile.cep = self.cleaned_data.get('cep', '')
            profile.whatsapp = self.cleaned_data.get('whatsapp', '')
            
            profile.save()
            
        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Nome de usuário',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu nome de usuário'
        })
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua senha'
        })
    )