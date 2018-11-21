# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):

    nome = models.CharField(max_length=255, null=False)
    key_stream = models.CharField(max_length=255, null=False)
    imagem_perfil = models.CharField(max_length=255, null=False)
    status = models.CharField(max_length=255, null=False)
    assistindo = models.CharField(max_length=255, null=True)
    usuario = models.OneToOneField(User, related_name="perfil", on_delete=models.PROTECT)

class Transmissao(models.Model):

    streamer = models.CharField(max_length=255, null=False)
    titulo = models.CharField(max_length=255, null=False)
    imagem = models.CharField(max_length=255, null=False)
    area = models.CharField(max_length=255, null=False)
    hrInicio = models.CharField(max_length=255, null=False)
    tempoLive = models.CharField(max_length=255, null=False)
    streamer_imagem = models.CharField(max_length=255, null=False)
    views = models.CharField(max_length=255, null=False)
    avaliacao = models.FloatField(null=False)

class Segue(models.Model):

    seguindo = models.CharField(max_length=255, null=False)
    seguidor = models.CharField(max_length=255, null=False)

class Chat(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=255)
    message = models.TextField()
    streamer_room = models.CharField(max_length=20)

    def __unicode__(self):
        return self.message

class Area(models.Model):

    area = models.CharField(max_length=100, null=False)
    imagem = models.CharField(max_length=100, null=False)

class Avaliacao(models.Model):

    nota = models.CharField(max_length=4, null=False)
    avaliado = models.CharField(max_length=1, null=False)
    avaliador = models.CharField(max_length=1, null=False)
