# Generated by Django 5.2 on 2025-07-06 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0008_cidade_produto_marca_alter_produto_cambio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='cidade',
            field=models.CharField(blank=True, max_length=100, verbose_name='Cidade'),
        ),
    ]
