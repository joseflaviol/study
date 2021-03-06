# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-25 13:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_transmissao_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='assistindo',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='imagem_perfil',
            field=models.CharField(default='img/icons/user.png', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='perfil',
            name='status',
            field=models.CharField(default='offline', max_length=255),
            preserve_default=False,
        ),
    ]
