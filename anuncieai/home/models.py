from django.db import models
from django.utils.translation import gettext_lazy as _

class CarouselSlide(models.Model):
    title = models.CharField(_('Título'), max_length=100)
    subtitle = models.CharField(_('Subtítulo'), max_length=200)
    badge_text = models.CharField(_('Texto do Badge'), max_length=50, blank=True)
    image = models.ImageField(_('Imagem'), upload_to='carousel/')
    button_text = models.CharField(_('Texto do Botão'), max_length=50, default='VER MAIS')
    button_url = models.CharField(_('URL do Botão'), max_length=200, default='produtos:loja')
    button_icon = models.CharField(_('Ícone do Botão'), max_length=50, default='fas fa-chevron-right')
    active = models.BooleanField(_('Ativo'), default=True)
    order = models.PositiveIntegerField(_('Ordem'), default=0)

    class Meta:
        verbose_name = _('Slide do Carrossel')
        verbose_name_plural = _('Slides do Carrossel')
        ordering = ['order']

    def __str__(self):
        return self.title