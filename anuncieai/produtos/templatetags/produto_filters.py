# produtos/templatetags/produto_filters.py
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Filtro para acessar um item de um dicionário usando uma chave.
    Exemplo de uso: {{ dict|get_item:key }}
    """
    return dictionary.get(key)