# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-30 13:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('key_stream', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=255, null=True)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Segue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seguindo', models.CharField(max_length=255)),
                ('seguidor', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Transmissao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('streamer', models.CharField(max_length=255)),
                ('titulo', models.CharField(max_length=255)),
                ('imagem', models.CharField(max_length=255)),
                ('area', models.CharField(max_length=255)),
                ('hrInicio', models.CharField(max_length=255)),
                ('hora', models.CharField(max_length=255)),
            ],
        ),
    ]