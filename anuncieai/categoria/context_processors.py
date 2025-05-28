from categoria.models import Categoria


def categorias_menu(request):
    lista_opcoes = Categoria.objects.all()
    return dict(opcoes = lista_opcoes)