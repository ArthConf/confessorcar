from django.db import models
from categoria.models import Categoria
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User

class ProdutoImagem(models.Model):
    produto = models.ForeignKey('Produto', related_name='imagens_produto', on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='fotos/produtos')
    ordem = models.IntegerField(default=0)

    class Meta:
        ordering = ['ordem']
        verbose_name = 'Imagem do Produto'
        verbose_name_plural = 'Imagens do Produto'


# Adicionar esta constante antes da classe Produto
ESTADO_CHOICES = [
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('AM', 'Amazonas'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranhão'),
    ('MT', 'Mato Grosso'),
    ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PR', 'Paraná'),
    ('PE', 'Pernambuco'),
    ('PI', 'Piauí'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'),
    ('SE', 'Sergipe'),
    ('TO', 'Tocantins'),
]
class Produto(models.Model):
    OPCIONAIS_CHOICES = [
        ("Ar-condicionado", "Ar-condicionado"),
        ("Ar-quente", "Ar-quente"),
        ("Direção hidráulica", "Direção hidráulica"),
        ("Direção elétrica", "Direção elétrica"),
        ("Vidros elétricos", "Vidros elétricos"),
        ("Travas elétricas", "Travas elétricas"),
        ("Bancos em couro", "Bancos em couro"),
        ("Banco do motorista com ajuste de altura", "Banco do motorista com ajuste de altura"),
        ("Banco traseiro bipartido", "Banco traseiro bipartido"),
        ("Computador de bordo", "Computador de bordo"),
        ("Câmbio automático", "Câmbio automático"),
        ("Câmbio CVT", "Câmbio CVT"),
        ("Câmbio manual", "Câmbio manual"),
        ("Controle de tração", "Controle de tração"),
        ("Controle de estabilidade", "Controle de estabilidade"),
        ("Airbag motorista", "Airbag motorista"),
        ("Airbag passageiro", "Airbag passageiro"),
        ("Airbags laterais", "Airbags laterais"),
        ("Airbags de cortina", "Airbags de cortina"),
        ("Freios ABS", "Freios ABS"),
        ("Assistente de partida em rampa", "Assistente de partida em rampa"),
        ("Sistema Start-Stop", "Sistema Start-Stop"),
        ("Sensor de estacionamento traseiro", "Sensor de estacionamento traseiro"),
        ("Sensor de estacionamento dianteiro", "Sensor de estacionamento dianteiro"),
        ("Câmera de ré", "Câmera de ré"),
        ("Farol de neblina", "Farol de neblina"),
        ("Faróis automáticos", "Faróis automáticos"),
        ("Faróis de LED", "Faróis de LED"),
        ("Lanternas em LED", "Lanternas em LED"),
        ("Rodas de liga leve", "Rodas de liga leve"),
        ("Teto solar", "Teto solar"),
        ("Teto panorâmico", "Teto panorâmico"),
        ("Piloto automático (Cruise control)", "Piloto automático (Cruise control)"),
        ("Limitador de velocidade", "Limitador de velocidade"),
        ("Central multimídia", "Central multimídia"),
        ("Bluetooth", "Bluetooth"),
        ("GPS integrado", "GPS integrado"),
        ("Entrada USB", "Entrada USB"),
        ("Carregador de celular por indução", "Carregador de celular por indução"),
        ("Retrovisores elétricos", "Retrovisores elétricos"),
        ("Retrovisores rebatíveis eletricamente", "Retrovisores rebatíveis eletricamente"),
        ("Desembaçador traseiro", "Desembaçador traseiro"),
        ("Sensor de chuva", "Sensor de chuva"),
        ("Sensor crepuscular", "Sensor crepuscular"),
        ("Chave presencial", "Chave presencial"),
        ("Partida sem chave (Start/Stop)", "Partida sem chave (Start/Stop)"),
        ("Alarme antifurto", "Alarme antifurto"),
        ("Isofix", "Isofix"),
        ("Volante com ajuste de altura", "Volante com ajuste de altura"),
        ("Volante com ajuste de profundidade", "Volante com ajuste de profundidade"),
        ("Controle de som no volante", "Controle de som no volante"),
        ("Assistente de frenagem de emergência", "Assistente de frenagem de emergência"),
        ("Controle automático de descida", "Controle automático de descida"),
        ("Reconhecimento de sinais de trânsito", "Reconhecimento de sinais de trânsito"),
        ("Alerta de ponto cego", "Alerta de ponto cego"),
        ("Alerta de mudança de faixa", "Alerta de mudança de faixa"),
        ("Assistente de permanência em faixa", "Assistente de permanência em faixa"),
        ("Detector de fadiga", "Detector de fadiga"),
        ("Freio de estacionamento eletrônico", "Freio de estacionamento eletrônico"),
        ("Display digital no painel", "Display digital no painel"),
        ("Head-up display", "Head-up display"),
        ("Ar-condicionado digital", "Ar-condicionado digital"),
        ("Ar-condicionado dual zone", "Ar-condicionado dual zone"),
        ("Suspensão adaptativa", "Suspensão adaptativa"),
        ("Acendimento automático dos faróis", "Acendimento automático dos faróis"),
        ("Encosto de cabeça para todos os ocupantes", "Encosto de cabeça para todos os ocupantes"),
        ("Rebatimento automático dos retrovisores", "Rebatimento automático dos retrovisores"),
        ("Para-brisa degradê", "Para-brisa degradê"),
        ("Tapetes personalizados", "Tapetes personalizados"),
        ("Protetor de cárter", "Protetor de cárter"),
        ("Engate para reboque", "Engate para reboque"),
    ]

    # Campos principais
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    produto_nome = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    descricao = models.TextField(max_length=500, blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    esta_disponivel = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    modificado_em = models.DateTimeField(auto_now=True)

    # Campos de usuário e localização
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='produtos')
    cidade = models.CharField('Cidade', max_length=100, blank=True)
    estado = models.CharField('Estado', max_length=2, choices=ESTADO_CHOICES, blank=True)

    # Campos de características do veículo
    CAMBIO_CHOICES = [
        ('manual', 'Manual'),
        ('automatico', 'Automático'),
        ('cvt', 'CVT'),
    ]
    
    CARROCERIA_CHOICES = [
        ('hatchback', 'Hatchback'),
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('pickup', 'Pickup'),
    ]
    
    COMBUSTIVEL_CHOICES = [
        ('flex', 'Flex'),
        ('gasolina', 'Gasolina'),
        ('diesel', 'Diesel'),
        ('eletrico', 'Elétrico'),
    ]

    cor = models.CharField('Cor', max_length=50, blank=True)
    ano_fabricacao = models.IntegerField('Ano de Fabricação', null=True, blank=True)
    ano_modelo = models.IntegerField('Ano do Modelo', null=True, blank=True)
    quilometragem = models.IntegerField('Quilometragem', null=True, blank=True)
    cambio = models.CharField('Câmbio', max_length=20, choices=CAMBIO_CHOICES, blank=True)
    carroceria = models.CharField('Carroceria', max_length=20, choices=CARROCERIA_CHOICES, blank=True)
    combustivel = models.CharField('Combustível', max_length=20, choices=COMBUSTIVEL_CHOICES, blank=True)
    placa_final = models.CharField('Final da Placa', max_length=1, blank=True)
    aceita_troca = models.BooleanField('Aceita Troca', default=False)
    ipva_pago = models.BooleanField('IPVA Pago', default=False)
    opcionais = models.JSONField('Opcionais', default=list, blank=True)
    
    # Campos adicionais para portas e motorização
    portas = models.PositiveSmallIntegerField('Número de Portas', blank=True, null=True)
    potencia = models.CharField('Potência do Motor', max_length=20, blank=True)
    cilindrada = models.CharField('Cilindrada', max_length=20, blank=True)

    def get_url(self):
        return reverse('produtos:produto_detalhe', args=[self.categoria.slug, self.slug])

    def get_primeira_imagem(self):
        primeira_imagem = self.imagens_produto.first()
        return primeira_imagem.imagem if primeira_imagem else None
        
    @property
    def localizacao(self):
        """Retorna a localização formatada: Cidade/Estado"""
        if self.cidade and self.estado:
            return f"{self.cidade}/{self.estado}"
        return "Não informado"
    
    @property
    def whatsapp(self):
        """Retorna o número de WhatsApp do anunciante"""
        if hasattr(self.user, 'profile') and self.user.profile.whatsapp:
            return self.user.profile.whatsapp
        return None
    
    @property
    def opcionais_list(self):
        """Retorna a lista de opcionais como uma lista de strings"""
        if isinstance(self.opcionais, list):
            return self.opcionais
        return []

    def __str__(self):
        return self.produto_nome

    def save(self, *args, **kwargs):
        # Gerar slug se não existir
        if not self.slug:
            self.slug = slugify(self.produto_nome)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ('-criado_em',)