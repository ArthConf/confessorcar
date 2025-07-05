from django.urls import path
from produtos import views

app_name = 'produtos'

urlpatterns = [
    # URLs existentes
    path('', views.visualizarLoja, name='loja'),
    path('gerenciar/', views.gerenciar_produtos, name='gerenciar_produtos'),
    path('adicionar/', views.adicionar_produto, name='adicionar_produto'),
    path('editar/<int:pk>/', views.editar_produto, name='editar_produto'),
    path('excluir/<int:pk>/', views.excluir_produto, name='excluir_produto'),
    path('<slug:categoria_slug>/', views.visualizarLoja, name='produto_por_categoria'),
    path('<slug:categoria_slug>/<slug:produto_slug>/', views.produto_detalhe, name='produto_detalhe'),
    path('produto/<int:pk>/marcar-vendido/', views.marcar_produto_vendido, name='marcar_vendido'),
    # Novas URLs para gerenciamento de imagens
    path('imagem/remover/<int:produto_pk>/<int:imagem_pk>/', 
         views.remover_imagem, 
         name='remover_imagem'),
    
    path('imagem/reordenar/<int:produto_pk>/', 
         views.reordenar_imagens, 
         name='reordenar_imagens'),
]