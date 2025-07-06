from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify
import json
import uuid
from .models import Produto, ProdutoImagem, MARCA_CHOICES, COR_CHOICES, ESTADO_CHOICES, Cidade

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class ProdutoImagemForm(forms.ModelForm):
    class Meta:
        model = ProdutoImagem
        fields = ['imagem']

class ProdutoForm(forms.ModelForm):
    # Removemos o campo slug do formulário para que ele não seja exibido
    # e seja gerado automaticamente
    cidade_texto = forms.CharField(
        label="Cidade",
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'id_cidade'  # Mantém o mesmo ID para compatibilidade com JavaScript
        })
    )

    imagens = MultipleFileField(
        required=False,
        widget=MultipleFileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        help_text='Você pode selecionar até 12 imagens'
    )
    
    opcionais = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'style': 'display:none;'
        })
    )

    class Meta:
        model = Produto
        fields = [
            'marca', 'produto_nome', 'categoria', 'descricao', 'preco',
            'estado', 'cidade_texto',  # substituir 'cidade' por 'cidade_texto'
            'cor', 'ano_fabricacao', 'ano_modelo', 'quilometragem',
            'portas', 'potencia', 'cilindrada',
            'cambio', 'combustivel', 'placa_final',
            'aceita_troca', 'ipva_pago', 'opcionais', 'esta_disponivel'
        ]
        widgets = {
            'marca': forms.Select(
                attrs={'class': 'form-select'},
                
            ),
            'produto_nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do Veículo'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descrição do veículo',
                'rows': 4
            }),
            'preco': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Preço'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select'
            }),
            'estado': forms.Select(
                attrs={'class': 'form-select'},
                choices=ESTADO_CHOICES
            ),
            'cor': forms.Select(
                attrs={'class': 'form-select'},
                choices=COR_CHOICES
            ),
            'ano_fabricacao': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ano de Fabricação'
            }),
            'ano_modelo': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ano do Modelo'
            }),
            'quilometragem': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Quilometragem'
            }),
            'portas': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de Portas',
                'min': 2,
                'max': 5
            }),
            'potencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 72cv'
            }),
            'cilindrada': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 1.0'
            }),
            'cambio': forms.Select(attrs={
                'class': 'form-select'
            }),
            'combustivel': forms.Select(attrs={
                'class': 'form-select'
            }),
            'placa_final': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Final da Placa',
                'maxlength': '1'
            }),
            'aceita_troca': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'ipva_pago': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'esta_disponivel': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Se estamos editando um produto com cidade
        if self.instance and self.instance.pk and self.instance.cidade:
            self.initial['cidade_texto'] = self.instance.cidade.nome
    
    def clean(self):
        cleaned_data = super().clean()
        cidade_texto = cleaned_data.get('cidade_texto')
        estado = cleaned_data.get('estado')
        
        # Se temos um nome de cidade e estado, buscar ou criar a cidade
        if cidade_texto and estado:
            try:
                cidade, created = Cidade.objects.get_or_create(
                    nome=cidade_texto,
                    estado=estado
                )
                # Adicionar a cidade ao cleaned_data
                cleaned_data['cidade'] = cidade
                print(f"Cidade processada: {cidade_texto}/{estado} (ID: {cidade.id}, Nova: {created})")
            except Exception as e:
                print(f"Erro ao criar/obter cidade: {e}")
                self.add_error('cidade_texto', "Erro ao processar cidade")
        
        return cleaned_data
    
    def save(self, commit=True):
        produto = super().save(commit=False)
        
        # Adicione este código para garantir que a cidade seja salva
        if 'cidade' in self.cleaned_data:
            produto.cidade = self.cleaned_data['cidade']
        
        # Resto do seu código...
        base_slug = slugify(produto.produto_nome)
        
        if not produto.slug:
            codigo_unico = str(uuid.uuid4())[:6]
            produto.slug = f"{base_slug}-{codigo_unico}"
        
        if not isinstance(produto.opcionais, list):
            produto.opcionais = self.cleaned_data.get('opcionais', [])
        
        if commit:
            produto.save()
            
        return produto

    def clean_opcionais(self):
        """
        Converte os opcionais recebidos para o formato esperado pelo JSONField
        """
        opcionais_data = self.cleaned_data.get('opcionais', '')
        print(f"Valor recebido em opcionais: {repr(opcionais_data)}")
        
        # Se já for uma lista, retornar como está
        if isinstance(opcionais_data, list):
            return opcionais_data
            
        # Tentar interpretar como JSON
        try:
            opcionais_json = json.loads(opcionais_data)
            if isinstance(opcionais_json, list):
                print(f"Convertido de JSON para lista: {opcionais_json}")
                return opcionais_json
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Erro ao tentar converter JSON: {e}")
            pass
        
        # Se falhou ao converter de JSON, tratar como texto com separadores
        if opcionais_data:
            resultado = [item.strip() for item in opcionais_data.split('\n') if item.strip()]
            print(f"Processado como texto separado: {resultado}")
            return resultado
            
        print("Retornando lista vazia para opcionais")
        return []

    def save(self, commit=True):
        produto = super().save(commit=False)
        
        # Gerar slug automaticamente
        base_slug = slugify(produto.produto_nome)
        
        # Adicionar um código curto único para diferenciar veículos do mesmo modelo
        # Formato: nome-do-veiculo-XYZ (onde XYZ é um código alfanumérico curto)
        codigo_unico = str(uuid.uuid4())[:6]  # Primeiros 6 caracteres do UUID
        
        # Para edição, verificamos se já existe um slug e se ele começa com o base_slug
        if produto.slug and produto.slug.startswith(base_slug):
            # Manter o mesmo código se estivermos editando
            pass
        else:
            # Novo produto ou nome mudou, criar novo slug
            produto.slug = f"{base_slug}-{codigo_unico}"
        
        # Garantir que opcionais seja uma lista antes de salvar
        if not isinstance(produto.opcionais, list):
            produto.opcionais = self.cleaned_data.get('opcionais', [])
        
        if commit:
            produto.save()
            
        return produto  