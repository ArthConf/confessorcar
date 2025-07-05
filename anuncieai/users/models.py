from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from localflavor.br.models import BRCPFField, BRStateField
from django.core.validators import RegexValidator

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    cpf = BRCPFField('CPF', help_text='Formato: 000.000.000-00', blank=True)
    endereco = models.CharField('Endereço', max_length=255, blank=True)
    bairro = models.CharField('Bairro', max_length=100, blank=True)
    cidade = models.CharField('Cidade', max_length=100, blank=True)
    estado = BRStateField('Estado', blank=True)
    cep = models.CharField('CEP', max_length=9, blank=True)
    
    phone_regex = RegexValidator(
        regex=r'^\(\d{2}\) \d{5}-\d{4}$',
        message="Formato: (99) 99999-9999"
    )
    whatsapp = models.CharField(
        'WhatsApp',
        validators=[phone_regex],
        max_length=15,
        blank=True,
        help_text='Formato: (99) 99999-9999'
    )
    
    avatar = models.ImageField(upload_to='fotos/usuarios', blank=True, null=True)
    data_registro = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Perfil de {self.user.username}'
        
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
        
# Sinais para criar/atualizar perfil quando um usuário é criado/atualizado
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()