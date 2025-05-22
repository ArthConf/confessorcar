from django.db import models
from categoria.models import Categoria 

class Produto(models.Model):
    categoria = models.ForeignKey(Categoria , on_delete=models.CASCADE)
    produto_nome = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True) #Um atributo que auxilia na criação da URL para acessar um produto
    descricao = models.TextField(max_length=300, unique=True)
    preco = models.DecimalField(max_digits=12, decimal_places=3)
    imagens = models.ImageField(upload_to = 'fotos/produtos')
    estoque = models.IntegerField()
    esta_disponivel = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    modificado_em = models.DateTimeField(auto_now_add=True)  
