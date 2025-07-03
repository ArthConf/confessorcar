from django import forms
from .models import Produto, ProdutoImagem

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
    imagens = MultipleFileField(
        required=False,
        widget=MultipleFileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        help_text='Você pode selecionar até 12 imagens'
    )
    
    opcionais = forms.MultipleChoiceField(
        choices=Produto.OPCIONAIS_CHOICES,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control select2',
            'data-placeholder': 'Selecione os opcionais'
        }),
        required=False
    )

    class Meta:
        model = Produto
        fields = [
            'produto_nome', 'slug', 'descricao', 'preco', 'categoria', 
            'cor', 'ano_fabricacao', 'ano_modelo', 'quilometragem', 
            'cambio', 'carroceria', 'combustivel', 'placa_final', 
            'aceita_troca', 'ipva_pago', 'opcionais', 'esta_disponivel'
        ]
        widgets = {
            'produto_nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do Veículo'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL amigável (slug)'
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
                'class': 'form-control'
            }),
            'cor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cor do veículo'
            }),
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
            'cambio': forms.Select(attrs={
                'class': 'form-control'
            }),
            'carroceria': forms.Select(attrs={
                'class': 'form-control'
            }),
            'combustivel': forms.Select(attrs={
                'class': 'form-control'
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

    def save(self, commit=True):
        produto = super().save(commit=commit)
        return produto