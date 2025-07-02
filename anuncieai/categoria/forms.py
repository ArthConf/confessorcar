from django import forms
from .models import Categoria

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['categoria_nome', 'slug', 'categoria_descricao', 'categoria_imagem']
        widgets = {
            'categoria_nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da Categoria'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL amigável (slug)'
            }),
            'categoria_descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descrição da categoria',
                'rows': 3
            }),
            'categoria_imagem': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }