from django.urls import path

from produtos import views

app_name = 'produtos'  # Adicione esta linha

urlpatterns = [
    path('',views.visualizarLoja, name='loja'),
    path('<slug:categoria_slug>/', views.visualizarLoja, name='produto_por_categoria'),
    path('<slug:categoria_slug>/<slug:produto_slug>/', views.produto_detalhe , name='produto_detalhe',)
]