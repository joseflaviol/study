# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from app.models import Chat, Transmissao, Perfil, Segue

admin.site.register(Chat)
admin.site.register(Transmissao)
admin.site.register(Perfil)
admin.site.register(Segue)
# Register your models here.
