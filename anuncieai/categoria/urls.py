from django.urls import path
from . import views

app_name = 'categoria'

urlpatterns = [
    path('gerenciar/', views.gerenciar_categorias, name='gerenciar_categorias'),
    path('adicionar/', views.adicionar_categoria, name='adicionar_categoria'),
    path('editar/<int:pk>/', views.editar_categoria, name='editar_categoria'),
    path('excluir/<int:pk>/', views.excluir_categoria, name='excluir_categoria'),
]