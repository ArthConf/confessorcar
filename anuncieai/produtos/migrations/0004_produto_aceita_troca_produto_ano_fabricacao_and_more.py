# Generated by Django 5.2 on 2025-07-03 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0003_alter_produto_options_alter_produto_descricao_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='aceita_troca',
            field=models.BooleanField(default=False, verbose_name='Aceita Troca'),
        ),
        migrations.AddField(
            model_name='produto',
            name='ano_fabricacao',
            field=models.IntegerField(blank=True, null=True, verbose_name='Ano de Fabricação'),
        ),
        migrations.AddField(
            model_name='produto',
            name='ano_modelo',
            field=models.IntegerField(blank=True, null=True, verbose_name='Ano do Modelo'),
        ),
        migrations.AddField(
            model_name='produto',
            name='cambio',
            field=models.CharField(blank=True, choices=[('manual', 'Manual'), ('automatico', 'Automático'), ('cvt', 'CVT')], max_length=20, verbose_name='Câmbio'),
        ),
        migrations.AddField(
            model_name='produto',
            name='carroceria',
            field=models.CharField(blank=True, choices=[('hatchback', 'Hatchback'), ('sedan', 'Sedan'), ('suv', 'SUV'), ('pickup', 'Pickup')], max_length=20, verbose_name='Carroceria'),
        ),
        migrations.AddField(
            model_name='produto',
            name='combustivel',
            field=models.CharField(blank=True, choices=[('flex', 'Gasolina e álcool'), ('gasolina', 'Gasolina'), ('diesel', 'Diesel'), ('eletrico', 'Elétrico')], max_length=20, verbose_name='Combustível'),
        ),
        migrations.AddField(
            model_name='produto',
            name='cor',
            field=models.CharField(blank=True, max_length=50, verbose_name='Cor'),
        ),
        migrations.AddField(
            model_name='produto',
            name='ipva_pago',
            field=models.BooleanField(default=False, verbose_name='IPVA Pago'),
        ),
        migrations.AddField(
            model_name='produto',
            name='opcionais',
            field=models.JSONField(blank=True, default=list, help_text='Lista de opcionais do veículo', verbose_name='Opcionais'),
        ),
        migrations.AddField(
            model_name='produto',
            name='placa_final',
            field=models.CharField(blank=True, max_length=1, verbose_name='Final da Placa'),
        ),
        migrations.AddField(
            model_name='produto',
            name='quilometragem',
            field=models.IntegerField(blank=True, null=True, verbose_name='Quilometragem'),
        ),
    ]
