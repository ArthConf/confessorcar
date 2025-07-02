from django.db import models
from categoria.models import Categoria
from django.urls import reverse
from django.utils.text import slugify

class Produto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    produto_nome = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    descricao = models.TextField(max_length=500, blank=True)  # Alterado
    preco = models.DecimalField(max_digits=10, decimal_places=2)  # Alterado
    imagens = models.ImageField(upload_to='fotos/produtos')
    esta_disponivel = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    modificado_em = models.DateTimeField(auto_now=True)  # Alterado

    def save(self, *args, **kwargs):  # Novo método
        if not self.slug:
            self.slug = slugify(self.produto_nome)
        super().save(*args, **kwargs)

    def get_url(self):  # Novo método
        return reverse('produtos:produto_detalhe', args=[self.categoria.slug, self.slug])

    def __str__(self):  # Novo método
        return self.produto_nome

    class Meta:  # Nova classe Meta
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ('-criado_em',)