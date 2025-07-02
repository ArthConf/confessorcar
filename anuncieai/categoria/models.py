from django.db import models
from django.urls import reverse

class Categoria(models.Model):
    categoria_nome = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=200, unique=True, null=True)
    categoria_descricao = models.TextField(max_length=250, blank=True)
    categoria_imagem = models.ImageField(upload_to='fotos/categorias', blank=True)
    
    class Meta:
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'
    
    def __str__(self):
        return self.categoria_nome
    
    def get_url(self):
        return reverse('produtos:produto_por_categoria', args=[self.slug])  # Adicionado namespace 'produtos:'