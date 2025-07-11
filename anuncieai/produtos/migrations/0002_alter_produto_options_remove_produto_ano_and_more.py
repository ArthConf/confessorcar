# Generated by Django 5.2 on 2025-07-02 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='produto',
            options={},
        ),
        migrations.RemoveField(
            model_name='produto',
            name='ano',
        ),
        migrations.RemoveField(
            model_name='produto',
            name='cambio',
        ),
        migrations.RemoveField(
            model_name='produto',
            name='carroceria',
        ),
        migrations.RemoveField(
            model_name='produto',
            name='combustivel',
        ),
        migrations.RemoveField(
            model_name='produto',
            name='cor',
        ),
        migrations.RemoveField(
            model_name='produto',
            name='quilometragem',
        ),
        migrations.AlterField(
            model_name='produto',
            name='descricao',
            field=models.TextField(max_length=300, unique=True),
        ),
        migrations.AlterField(
            model_name='produto',
            name='modificado_em',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
