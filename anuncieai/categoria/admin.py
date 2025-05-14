from django.contrib import admin

from .models import Categoria

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('categoria_nome',)
admin.site.register(Categoria, CategoriaAdmin)

