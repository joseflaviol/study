# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-27 19:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20180825_1326'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.CharField(max_length=100)),
                ('imagem', models.CharField(max_length=100)),
            ],
        ),
    ]
