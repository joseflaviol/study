from django.conf.urls import url, include
from django.contrib import admin
from app import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^streams$', views.streams, name="streams"),
    url(r'^mini/$', views.mini, name="mini"),
    url(r'^mini/(?P<busca>.+)$', views.miniBusca, name="miniBusca"),
    url(r'^canal/(?P<streamer_nome>.+)$', views.canal, name="canal"),
    url(r'^live/(?P<streamer_id>\d+)$', views.live, name="live"),
    url(r'^player/(?P<streamer_id>\d+)$', views.player, name="player"),
    url(r'^chat/(?P<streamer_id>\d+)$', views.chat, name="chat"),
    #url(r'^chat/$', views.chat, name="chat"),
    url(r'^cadastro/(?P<page>.+)/$', views.cadastro, name="cadastro"),
    url(r'^login/(?P<page>.+)/$', views.login_view, name="login"),
    url(r'^logout/(?P<page>.+)/$', views.logout_view, name="logout"),
    url(r'^iniciaStream/$', views.iniciaStream, name="iniciaStream"),
    url(r'^encerraStream/$', views.encerraStream, name="encerraStream"),
    url(r'^seguir/$', views.seguir, name="seguir"),
    url(r'^unfollow/$', views.unfollow, name="unfollow"),
    url(r'^teste/$', views.teste, name="teste"),
    url(r'^ajax/$', views.ajax, name="ajax"),
    url(r'^validaCadastro/$', views.validaCadastro, name="validaCadastro"),
    url(r'^validaLogin/$', views.validaLogin, name="validaLogin"),
    url(r'^postMsg/(?P<streamer_id>\d+)$', views.PostMsg, name='postMsg'),
    url(r'^messages/(?P<streamer_id>\d+)$', views.Messages, name='messages'),
    url(r'^atualizaFiltro/$', views.atualizaFiltro, name="atualizaFiltro"),
    url(r'^painel/(?P<streamer_nome>.+)$', views.painel, name="painel"),
    url(r'^userIframe/$', views.userIframe, name="userIframe"),
    url(r'^userTutorial/$', views.userTutorial, name="userTutorial"),
    url(r'^obsS/$', views.obsS, name="obsS"),
    url(r'^config/$', views.config, name="config"),
    url(r'^avaliacao/$', views.avaliacao, name="avaliacao"),
    url(r'^mudaFoto/$', views.mudaFoto, name="mudaFoto"),
    url(r'^mudaFotoUser/$', views.mudaFotoUser, name="mudaFotoUser"),
    url(r'^atualizaStreamDados/$', views.atualizaDadosStream, name="atualizaStreamDados"),
    url(r'^atualizaDadosUser/$', views.atualizaDadosUser, name="atualizaDadosUser")
]