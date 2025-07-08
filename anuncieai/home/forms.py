from django import forms
from .models import CarouselSlide

class CarouselSlideForm(forms.ModelForm):
    class Meta:
        model = CarouselSlide
        fields = [
            'title', 'subtitle', 'badge_text', 'image',
            'button_text', 'button_url', 'button_filters', 'button_icon',
            'active', 'order'
        ]