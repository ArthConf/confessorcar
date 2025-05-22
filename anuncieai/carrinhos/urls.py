from django.urls import path
from carrinhos import views

urlpatterns = [
    path('',views.visualizarCarrinho, name = 'carrinho'),
]