# Generated by Django 4.2.11 on 2025-05-06 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verhalen', '0002_verhaal_is_spotlighted'),
    ]

    operations = [
        migrations.AddField(
            model_name='verhaal',
            name='is_downloadable',
            field=models.BooleanField(default=False),
        ),
    ]
