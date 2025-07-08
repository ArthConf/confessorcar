# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile

# Define um ModelAdmin para o modelo Profile
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'whatsapp', 'cpf', 'cidade', 'estado')
    search_fields = ('user__username', 'user__email', 'whatsapp', 'cpf')
    list_filter = ('estado',)

# Registrar o ModelAdmin para Profile
admin.site.register(Profile, ProfileAdmin)

# Define um InlineAdmin para Profile dentro do UserAdmin
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'perfis'

# Define uma classe UserAdmin customizada
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_whatsapp')
    
    def get_whatsapp(self, obj):
        try:
            return obj.profile.whatsapp
        except Profile.DoesNotExist:
            return 'Sem perfil'
    
    get_whatsapp.short_description = 'WhatsApp'
    get_whatsapp.admin_order_field = 'profile__whatsapp'

# Re-registrar o User com o novo UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)