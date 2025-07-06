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

# Lista de estados
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

# Lista de cores
COR_CHOICES = [
    ('preto', 'Preto'),
    ('branco', 'Branco'),
    ('prata', 'Prata'),
    ('cinza', 'Cinza'),
    ('vermelho', 'Vermelho'),
    ('azul', 'Azul'),
    ('azul_marinho', 'Azul Marinho'),
    ('azul_claro', 'Azul Claro'),
    ('verde', 'Verde'),
    ('verde_escuro', 'Verde Escuro'),
    ('verde_militar', 'Verde Militar'),
    ('amarelo', 'Amarelo'),
    ('laranja', 'Laranja'),
    ('marrom', 'Marrom'),
    ('bege', 'Bege'),
    ('dourado', 'Dourado'),
    ('grafite', 'Grafite'),
    ('vinho', 'Vinho'),
    ('bordô', 'Bordô'),
    ('bronze', 'Bronze'),
    ('chumbo', 'Chumbo'),
    ('champagne', 'Champagne'),
    ('rosa', 'Rosa'),
    ('roxo', 'Roxo'),
    ('violeta', 'Violeta'),
    ('cinza_escuro', 'Cinza Escuro'),
    ('cinza_claro', 'Cinza Claro'),
    ('marfim', 'Marfim'),
    ('titanium', 'Titanium'),
    ('prata_fosco', 'Prata Fosco'),
    ('preto_fosco', 'Preto Fosco'),
]

# Lista completa de marcas de automóveis
MARCA_CHOICES = [
    # Marcas Nacionais e Populares no Brasil
    ('chevrolet', 'Chevrolet'),
    ('fiat', 'Fiat'),
    ('ford', 'Ford'),
    ('volkswagen', 'Volkswagen'),
    ('renault', 'Renault'),
    ('toyota', 'Toyota'),
    ('hyundai', 'Hyundai'),
    ('honda', 'Honda'),
    ('nissan', 'Nissan'),
    ('citroen', 'Citroën'),
    ('peugeot', 'Peugeot'),
    ('mitsubishi', 'Mitsubishi'),
    
    # Marcas Premium
    ('audi', 'Audi'),
    ('bmw', 'BMW'),
    ('mercedes', 'Mercedes-Benz'),
    ('land_rover', 'Land Rover'),
    ('volvo', 'Volvo'),
    ('lexus', 'Lexus'),
    ('porsche', 'Porsche'),
    ('jaguar', 'Jaguar'),
    ('maserati', 'Maserati'),
    ('ferrari', 'Ferrari'),
    ('lamborghini', 'Lamborghini'),
    ('bentley', 'Bentley'),
    ('rolls_royce', 'Rolls-Royce'),
    ('aston_martin', 'Aston Martin'),
    
    # Marcas Asiáticas
    ('kia', 'Kia'),
    ('subaru', 'Subaru'),
    ('suzuki', 'Suzuki'),
    ('mazda', 'Mazda'),
    ('jac', 'JAC'),
    ('chery', 'Chery'),
    ('lifan', 'Lifan'),
    ('byd', 'BYD'),
    ('geely', 'Geely'),
    ('great_wall', 'Great Wall'),
    ('haval', 'Haval'),
    ('saic', 'SAIC'),
    ('dongfeng', 'Dongfeng'),
    ('ssangyong', 'SsangYong'),
    ('tata', 'Tata'),
    ('mahindra', 'Mahindra'),
    ('isuzu', 'Isuzu'),
    ('daihatsu', 'Daihatsu'),
    
    # Marcas Americanas
    ('jeep', 'Jeep'),
    ('chrysler', 'Chrysler'),
    ('dodge', 'Dodge'),
    ('cadillac', 'Cadillac'),
    ('gmc', 'GMC'),
    ('lincoln', 'Lincoln'),
    ('tesla', 'Tesla'),
    ('ram', 'RAM'),
    ('buick', 'Buick'),
    
    # Marcas Europeias
    ('alfa_romeo', 'Alfa Romeo'),
    ('seat', 'Seat'),
    ('skoda', 'Skoda'),
    ('mini', 'Mini'),
    ('smart', 'Smart'),
    ('ds', 'DS'),
    ('opel', 'Opel'),
    ('fiat_professional', 'Fiat Professional'),
    ('dacia', 'Dacia'),
    ('lada', 'Lada'),
    
    # Marcas Brasileiras
    ('troller', 'Troller'),
    ('agrale', 'Agrale'),
    ('marcopolo', 'Marcopolo'),
    ('gurgel', 'Gurgel'),
    ('puma', 'Puma'),
    
    # Caminhões e Comerciais
    ('scania', 'Scania'),
    ('volvo_trucks', 'Volvo Trucks'),
    ('mercedes_benz_trucks', 'Mercedes-Benz Trucks'),
    ('iveco', 'Iveco'),
    ('daf', 'DAF'),
    ('man', 'MAN'),
    ('volkswagen_trucks', 'Volkswagen Trucks'),
    ('hino', 'Hino'),
    
    # Outros
    ('caoa', 'CAOA'),
    ('outros', 'Outros'),
]

MARCA_CHOICES = sorted(MARCA_CHOICES, key=lambda x: x[1].lower())

class Cidade(models.Model):
    """
    Modelo para armazenar cidades por estado para uso com API
    """
    nome = models.CharField(max_length=100)
    estado = models.CharField(max_length=2, choices=ESTADO_CHOICES)

    def __str__(self):
        return f"{self.nome}/{self.estado}"

    class Meta:
        verbose_name = 'Cidade'
        verbose_name_plural = 'Cidades'
        ordering = ['estado', 'nome']

class Produto(models.Model):
    # Opcionais categorizados
    OPCIONAIS_CONFORTO = [
        ("Ar-condicionado", "Ar-condicionado"),
        ("Ar-condicionado digital", "Ar-condicionado digital"),
        ("Ar-condicionado dual zone", "Ar-condicionado dual zone"),
        ("Ar-condicionado tri zone", "Ar-condicionado tri zone"),
        ("Ar-condicionado quad zone", "Ar-condicionado quad zone"),
        ("Ar-quente", "Ar-quente"),
        ("Bancos com regulagem elétrica", "Bancos com regulagem elétrica"),
        ("Bancos com ajuste lombar", "Bancos com ajuste lombar"),
        ("Bancos com memória", "Bancos com memória"),
        ("Bancos com massagem", "Bancos com massagem"),
        ("Bancos com ventilação", "Bancos com ventilação"),
        ("Bancos com aquecimento", "Bancos com aquecimento"),
        ("Bancos em couro", "Bancos em couro"),
        ("Bancos em couro sintético", "Bancos em couro sintético"),
        ("Bancos rebatíveis", "Bancos rebatíveis"),
        ("Banco do motorista com ajuste de altura", "Banco do motorista com ajuste de altura"),
        ("Banco traseiro bipartido", "Banco traseiro bipartido"),
        ("Direção hidráulica", "Direção hidráulica"),
        ("Direção elétrica", "Direção elétrica"),
        ("Vidros elétricos", "Vidros elétricos"),
        ("Vidros elétricos dianteiros", "Vidros elétricos dianteiros"),
        ("Vidros elétricos traseiros", "Vidros elétricos traseiros"),
        ("Vidros elétricos com one touch", "Vidros elétricos com one touch"),
        ("Travas elétricas", "Travas elétricas"),
        ("Volante com ajuste de altura", "Volante com ajuste de altura"),
        ("Volante com ajuste de profundidade", "Volante com ajuste de profundidade"),
        ("Volante em couro", "Volante em couro"),
        ("Teto solar", "Teto solar"),
        ("Teto panorâmico", "Teto panorâmico"),
        ("Retrovisores elétricos", "Retrovisores elétricos"),
        ("Retrovisores rebatíveis eletricamente", "Retrovisores rebatíveis eletricamente"),
        ("Retrovisores com aquecimento", "Retrovisores com aquecimento"),
        ("Retrovisores com memória", "Retrovisores com memória"),
        ("Porta-malas com abertura elétrica", "Porta-malas com abertura elétrica"),
        ("Porta-malas com sensor de presença", "Porta-malas com sensor de presença"),
        ("Abertura das portas por proximidade", "Abertura das portas por proximidade"),
    ]

    OPCIONAIS_SEGURANCA = [
        ("Airbag motorista", "Airbag motorista"),
        ("Airbag passageiro", "Airbag passageiro"),
        ("Airbags laterais", "Airbags laterais"),
        ("Airbags de cortina", "Airbags de cortina"),
        ("Airbag de joelho", "Airbag de joelho"),
        ("Freios ABS", "Freios ABS"),
        ("EBD - Distribuição eletrônica de frenagem", "EBD - Distribuição eletrônica de frenagem"),
        ("Assistente de frenagem de emergência", "Assistente de frenagem de emergência"),
        ("Controle de tração", "Controle de tração"),
        ("Controle de estabilidade", "Controle de estabilidade"),
        ("Assistente de partida em rampa", "Assistente de partida em rampa"),
        ("Controle automático de descida", "Controle automático de descida"),
        ("Sensor de estacionamento traseiro", "Sensor de estacionamento traseiro"),
        ("Sensor de estacionamento dianteiro", "Sensor de estacionamento dianteiro"),
        ("Câmera de ré", "Câmera de ré"),
        ("Câmeras 360 graus", "Câmeras 360 graus"),
        ("Alerta de ponto cego", "Alerta de ponto cego"),
        ("Alerta de mudança de faixa", "Alerta de mudança de faixa"),
        ("Assistente de permanência em faixa", "Assistente de permanência em faixa"),
        ("Detector de fadiga", "Detector de fadiga"),
        ("Reconhecimento de sinais de trânsito", "Reconhecimento de sinais de trânsito"),
        ("Frenagem automática de emergência", "Frenagem automática de emergência"),
        ("Detector de pedestres", "Detector de pedestres"),
        ("Detector de ciclistas", "Detector de ciclistas"),
        ("Piloto automático adaptativo", "Piloto automático adaptativo"),
        ("Sistema de detecção de tráfego cruzado", "Sistema de detecção de tráfego cruzado"),
        ("Sistema de estacionamento automático", "Sistema de estacionamento automático"),
        ("Isofix", "Isofix"),
        ("Alarme antifurto", "Alarme antifurto"),
        ("Bloqueio de motor", "Bloqueio de motor"),
        ("Sistema de rastreamento", "Sistema de rastreamento"),
        ("Monitoramento de pressão dos pneus", "Monitoramento de pressão dos pneus"),
        ("Farol de neblina", "Farol de neblina"),
        ("Faróis de LED", "Faróis de LED"),
        ("Faróis automáticos", "Faróis automáticos"),
        ("Faróis com ajuste de altura", "Faróis com ajuste de altura"),
        ("Faróis direcionais", "Faróis direcionais"),
        ("Faróis com acendimento automático", "Faróis com acendimento automático"),
        ("Lanternas em LED", "Lanternas em LED"),
        ("Luzes de condução diurna (DRL)", "Luzes de condução diurna (DRL)"),
    ]

    OPCIONAIS_TECNOLOGIA = [
        ("Computador de bordo", "Computador de bordo"),
        ("Central multimídia", "Central multimídia"),
        ("Central multimídia com touchscreen", "Central multimídia com touchscreen"),
        ("Android Auto", "Android Auto"),
        ("Apple CarPlay", "Apple CarPlay"),
        ("Bluetooth", "Bluetooth"),
        ("GPS integrado", "GPS integrado"),
        ("GPS integrado com atualizações online", "GPS integrado com atualizações online"),
        ("Entrada USB", "Entrada USB"),
        ("Entrada HDMI", "Entrada HDMI"),
        ("Entrada auxiliar", "Entrada auxiliar"),
        ("Sistema de som premium", "Sistema de som premium"),
        ("Sistema de som com múltiplos alto-falantes", "Sistema de som com múltiplos alto-falantes"),
        ("Sistema de som com subwoofer", "Sistema de som com subwoofer"),
        ("Controle de som no volante", "Controle de som no volante"),
        ("Display digital no painel", "Display digital no painel"),
        ("Head-up display", "Head-up display"),
        ("Sistema Start-Stop", "Sistema Start-Stop"),
        ("Sensor de chuva", "Sensor de chuva"),
        ("Sensor crepuscular", "Sensor crepuscular"),
        ("Chave presencial", "Chave presencial"),
        ("Partida sem chave (Start/Stop)", "Partida sem chave (Start/Stop)"),
        ("Carregador de celular por indução", "Carregador de celular por indução"),
        ("Tomada 12V", "Tomada 12V"),
        ("Piloto automático (Cruise control)", "Piloto automático (Cruise control)"),
        ("Limitador de velocidade", "Limitador de velocidade"),
        ("Freio de estacionamento eletrônico", "Freio de estacionamento eletrônico"),
        ("Auto hold", "Auto hold"),
        ("Assistente de estacionamento", "Assistente de estacionamento"),
        ("Câmbio borboleta", "Câmbio borboleta"),
        ("Paddle shift", "Paddle shift"),
        ("Seleção de modos de condução", "Seleção de modos de condução"),
        ("Sistema de navegação", "Sistema de navegação"),
        ("Wi-Fi integrado", "Wi-Fi integrado"),
        ("Sistema de som com cancelamento de ruído", "Sistema de som com cancelamento de ruído"),
        ("Tela para passageiros traseiros", "Tela para passageiros traseiros"),
    ]

    OPCIONAIS_OUTROS = [
        ("Rodas de liga leve", "Rodas de liga leve"),
        ("Rodas de liga leve aro 15", "Rodas de liga leve aro 15"),
        ("Rodas de liga leve aro 16", "Rodas de liga leve aro 16"),
        ("Rodas de liga leve aro 17", "Rodas de liga leve aro 17"),
        ("Rodas de liga leve aro 18", "Rodas de liga leve aro 18"),
        ("Rodas de liga leve aro 19", "Rodas de liga leve aro 19"),
        ("Rodas de liga leve aro 20", "Rodas de liga leve aro 20"),
        ("Rodas de liga leve aro 21", "Rodas de liga leve aro 21"),
        ("Rodas de liga leve aro 22", "Rodas de liga leve aro 22"),
        ("Suspensão adaptativa", "Suspensão adaptativa"),
        ("Suspensão rebaixada", "Suspensão rebaixada"),
        ("Suspensão elevada", "Suspensão elevada"),
        ("Suspensão a ar", "Suspensão a ar"),
        ("Câmbio automático", "Câmbio automático"),
        ("Câmbio CVT", "Câmbio CVT"),
        ("Câmbio manual", "Câmbio manual"),
        ("Câmbio automatizado", "Câmbio automatizado"),
        ("Câmbio dupla embreagem", "Câmbio dupla embreagem"),
        ("Para-brisa degradê", "Para-brisa degradê"),
        ("Vidros escurecidos", "Vidros escurecidos"),
        ("Vidros blindados", "Vidros blindados"),
        ("Tapetes personalizados", "Tapetes personalizados"),
        ("Protetor de cárter", "Protetor de cárter"),
        ("Protetor de caçamba", "Protetor de caçamba"),
        ("Engate para reboque", "Engate para reboque"),
        ("Santo Antônio", "Santo Antônio"),
        ("Estribo", "Estribo"),
        ("Bagageiro de teto", "Bagageiro de teto"),
        ("Rack de teto", "Rack de teto"),
        ("Capota marítima", "Capota marítima"),
        ("Capota rígida", "Capota rígida"),
        ("Desembaçador traseiro", "Desembaçador traseiro"),
        ("Brake light", "Brake light"),
        ("Spoiler traseiro", "Spoiler traseiro"),
        ("Aerofólio", "Aerofólio"),
        ("Rebatimento automático dos retrovisores", "Rebatimento automático dos retrovisores"),
        ("Encosto de cabeça para todos os ocupantes", "Encosto de cabeça para todos os ocupantes"),
        ("Kit esportivo", "Kit esportivo"),
        ("Kit off-road", "Kit off-road"),
        ("Adesivos personalizados", "Adesivos personalizados"),
        ("Jogo de calotas", "Jogo de calotas"),
        ("Pintura metálica", "Pintura metálica"),
        ("Pintura perolizada", "Pintura perolizada"),
    ]

    # Combinar todas as categorias de opcionais
    OPCIONAIS_CHOICES = OPCIONAIS_CONFORTO + OPCIONAIS_SEGURANCA + OPCIONAIS_TECNOLOGIA + OPCIONAIS_OUTROS

    # Campos principais
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    produto_nome = models.CharField(max_length=200)
    marca = models.CharField('Marca', max_length=100, choices=MARCA_CHOICES, blank=True)
    slug = models.SlugField(max_length=200, unique=True)
    descricao = models.TextField(max_length=500, blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    esta_disponivel = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    modificado_em = models.DateTimeField(auto_now=True)

    # Campos de usuário e localização
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='produtos')
    cidade = models.ForeignKey(Cidade, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Cidade')
    estado = models.CharField('Estado', max_length=2, choices=ESTADO_CHOICES, blank=True)

    # Campos de características do veículo
    CAMBIO_CHOICES = [
        ('manual', 'Manual'),
        ('automatico', 'Automático'),
        ('cvt', 'CVT'),
        ('automatizado', 'Automatizado'),
        ('semi_automatico', 'Semi-Automático'),
        ('dupla_embreagem', 'Dupla Embreagem'),
    ]
    
    CARROCERIA_CHOICES = [
        ('hatchback', 'Hatchback'),
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('crossover', 'Crossover'),
        ('pickup', 'Pickup'),
        ('minivan', 'Minivan'),
        ('van', 'Van'),
        ('perua', 'Perua/SW'),
        ('coupe', 'Coupé'),
        ('conversivel', 'Conversível'),
        ('jipe', 'Jipe'),
        ('buggy', 'Buggy'),
        ('esportivo', 'Esportivo'),
        ('utilitario', 'Utilitário'),
        ('caminhao', 'Caminhão'),
        ('outro', 'Outro'),
    ]
    
    COMBUSTIVEL_CHOICES = [
        ('flex', 'Flex'),
        ('gasolina', 'Gasolina'),
        ('diesel', 'Diesel'),
        ('eletrico', 'Elétrico'),
        ('hibrido', 'Híbrido'),
        ('hibrido_plug_in', 'Híbrido Plug-in'),
        ('etanol', 'Etanol'),
        ('gnv', 'GNV'),
        ('outro', 'Outro'),
    ]

    cor = models.CharField('Cor', max_length=50, choices=COR_CHOICES, blank=True)
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
        primeira_imagem = self.imagens_produto.order_by('ordem').first()
        return primeira_imagem.imagem if primeira_imagem else None
        
    @property
    def localizacao(self):
        """Retorna a localização formatada: Cidade/Estado"""
        if self.cidade:
            return f"{self.cidade.nome}/{self.cidade.estado}"
        elif self.estado:
            return f"/{self.estado}"
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
    
    @property
    def opcionais_por_categoria(self):
        """Retorna os opcionais organizados por categoria"""
        if not isinstance(self.opcionais, list):
            return {}
            
        result = {
            'conforto': [],
            'seguranca': [],
            'tecnologia': [],
            'outros': []
        }
        
        opcionais_conforto = [op[0] for op in self.OPCIONAIS_CONFORTO]
        opcionais_seguranca = [op[0] for op in self.OPCIONAIS_SEGURANCA]
        opcionais_tecnologia = [op[0] for op in self.OPCIONAIS_TECNOLOGIA]
        
        for opcional in self.opcionais:
            if opcional in opcionais_conforto:
                result['conforto'].append(opcional)
            elif opcional in opcionais_seguranca:
                result['seguranca'].append(opcional)
            elif opcional in opcionais_tecnologia:
                result['tecnologia'].append(opcional)
            else:
                result['outros'].append(opcional)
                
        return result

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