from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['produto_nome', 'slug', 'descricao', 'preco', 'imagens', 'categoria', 'esta_disponivel']
        widgets = {
            'produto_nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do Produto'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL amigável (slug)'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descrição do produto',
                'rows': 4
            }),
            'preco': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Preço'
            }),
            'imagens': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-control'
            }),
            'esta_disponivel': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }