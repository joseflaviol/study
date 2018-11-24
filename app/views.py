# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import datetime
import json
import glob
from random import choice
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from app.models import Perfil, Transmissao, Segue, Chat, Area, Avaliacao
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.hashers import make_password

def index(request):
    return render(request, "index.html", {"perfil_logado" : perfil_logado(request)})

def userDados(request):
    perfil = perfil_logado(request)
    dados = User.objects.get(username__exact=perfil.nome)
    return dados

def streams(request):
    busca = None
    perfil = None
    transmissao = []
    area = Area.objects.all()
    numeroArea = len(area)
    atualizaViews(request)
    if 'buscar' in request.POST:
        busca = request.POST['buscar']
    try:
        perfil = perfil_logado(request)
        perfil.assistindo = ""
        perfil.save()
        segue = Segue.objects.filter(seguidor=perfil.nome)
        for row in segue:
            stream = Transmissao.objects.filter(streamer=row.seguindo)
            perfil = Perfil.objects.get(nome=row.seguindo)
            for campo in stream:
                transmissao.append(campo)
    except Exception as e:
        pass

    return render(request, "streams.html", {"perfil_logado" : perfil_logado(request), "perfil_status": perfil_status(request), "busca":busca, "transmissao": transmissao, "destaque": Transmissao.objects.all(), "area": area, "numeroArea": numeroArea})

def atualizaTempo(request):
    streams = Transmissao.objects.all()
    for row in streams:
        dia = 0
        x = datetime.datetime.strptime(row.hrInicio, '%Y-%m-%d %H:%M:%S.%f')
        diff = datetime.datetime.now() - x
        try:
            diff = datetime.datetime.strptime(str(diff), '%H:%M:%S.%f')
        except Exception as e:
            diff = datetime.datetime.strptime(str(diff), '%d days, %H:%M:%S.%f')
            dia = diff.day
        hora = diff.hour
        min = diff.minute
        if int(dia) > 0:
            msg = str(dia)+"d, "+str(hora)+"h e "+str(min)+"min"
        elif int(hora) > 0:
            msg = str(hora)+"h e "+str(min)+"min"
        else:
            msg = str(min)+"min"
        row.tempoLive = msg
        row.save()

def mini(request):
    streams = Transmissao.objects.all()

    atualizaViews(request)

    atualizaTempo(request)

    area = Area.objects.all()
    nArea = len(area)

    return render(request, "mini.html", {"streams": streams, "nArea": nArea, "area": area})

def miniBusca(request, busca):
    buscaResult = None
    area = Area.objects.all()
    nArea = len(area)
    atualizaViews(request)
    try:
        buscaResult = Transmissao.objects.filter(streamer__startswith=busca)
    except Exception as e:
        pass

    return render(request, "mini.html", {"busca" : busca, "streams" : buscaResult, "nArea": nArea, "area": area})

def canal(request, streamer_nome):
    streamer = None
    transmissao = []
    area = Area.objects.all()
    nArea = len(area)
    try:
        streamer = Perfil.objects.get(nome=streamer_nome)
        perfil = perfil_logado(request)
        if streamer.status == "streaming":
            s = Transmissao.objects.get(streamer=streamer_nome)
            perfil.assistindo = s.id
            perfil.save()
        segue = Segue.objects.filter(seguidor=perfil.nome)
        for row in segue:
            stream = Transmissao.objects.filter(streamer=row.seguindo)
            for campo in stream:
                transmissao.append(campo)
        return render(request, "canal.html", {"perfil_logado": perfil_logado(request), "perfil_status": perfil_status(request), "streamer": streamer, "destaque": Transmissao.objects.all(), "transmissao": transmissao, "area": area, "nArea": nArea})
    except Exception as e:
        return render(request, "canal.html", {"perfil_logado": perfil_logado(request), "perfil_status": perfil_status(request), "streamer": streamer, "destaque": Transmissao.objects.all(), "area": area, "nArea": nArea})

def live(request, streamer_id):
    try:
        streamer = Perfil.objects.get(id=streamer_id)
        return render(request, "live.html", {"perfil_logado": perfil_logado(request), "streamer": streamer})
    except Exception as e:
        raise

def atualizaViews(request):
    streams = Transmissao.objects.all()
    for row in streams:
        views = 0
        perfil_all = Perfil.objects.filter(assistindo=row.id)
        for p in perfil_all:
            views = views + 1
        row.views = views
        row.save()

def player(request, streamer_id):
    stream = None
    perfil = None
    numero_seguidores = 0
    botao_seguir = None
    views = 0
    streaming = None
    contAvaliacao = 0
    nota = None
    avaliou = None
    area = None
    streamer = Perfil.objects.get(id=streamer_id)
    if Avaliacao.objects.filter(avaliado=streamer.id):
        avaliacao = Avaliacao.objects.filter(avaliado=streamer.id)
        for row in avaliacao:
            contAvaliacao += float(row.nota)
        nota = contAvaliacao/len(avaliacao)
        if len(str(nota)) > 3:
            nota = round(nota, 1)
    if streamer.status == "streaming":
        streaming = True
    if perfil_logado(request):
        perfil = request.user.perfil
        botao_seguir = Segue.objects.filter(seguindo=streamer.nome, seguidor=perfil.nome)
        if Avaliacao.objects.filter(avaliado=streamer.id, avaliador=perfil.id):
            avaliou = True
    seguidores = Segue.objects.filter(seguindo=streamer.nome)
    for row in seguidores:
        numero_seguidores = numero_seguidores + 1
    try:
        stream = Transmissao.objects.get(streamer=streamer.nome)
        stream.avaliacao = nota
        stream.save()
        if  Area.objects.filter(area=stream.area):
            area = Area.objects.get(area=stream.area)
        return render(request, "player.html", {"perfil_logado": perfil_logado(request), "avaliou": avaliou, "nota": nota, "streamer": streamer, "stream": stream, "seguidores": numero_seguidores, "botao_seguir": botao_seguir, "area": area, "streaming": streaming})
    except Exception as e:
        if Transmissao.objects.filter(streamer=streamer.nome):
            stream = Transmissao.objects.get(streamer=streamer.nome)
            if nota is not None:
                stream.avaliacao = nota
            else:
                stream.avaliacao = "0"
            stream.save()
            perfil.assistindo = stream.id
            perfil.save()
            atualizaViews(request)
            if Area.objects.filter(area=stream.area):
                area = Area.objects.get(area=stream.area)
            else:
                area = None
        else:
            stream = None
        return render(request, "player.html", {"perfil_logado": perfil_logado(request), "avaliou": avaliou, "nota": nota, "streamer": streamer, "stream": stream, "seguidores": numero_seguidores, "botao_seguir": botao_seguir, "area": area, "streaming": streaming})

def perfil_logado(request):
    if request.user.is_authenticated:
        return request.user.perfil
    else:
        return None

def perfil_status(request):
    if request.user.is_authenticated:
        perfil = request.user.perfil
        if perfil.status == "online":
            return True
        else:
            return None
    else:
        None

def gera_senha():
        caracters = '0123456789abcdefghijlmnopqrstuwvxz'
        senha = ''
        for char in range(10):
                senha += choice(caracters)
        return  senha

def cadastro(request, page):
    try:
        username = request.POST['username']
        password = request.POST['password']
        confPass = request.POST['confPass']
        email = request.POST['email']

        if password != confPass:
            return redirect('index')
        else:
            usuario = User.objects.create_user(username, email, password)
            usuario = authenticate(request, username=username, password=password)
            login(request, usuario)
            key_stream = "STUDY"+gera_senha()
            perfil = Perfil(nome=username, key_stream=key_stream, usuario=usuario, status="online", imagem_perfil="img/icons/user.png")
            perfil.save()
            os.makedirs("app/static/users/"+username)
            if page == "index" or page == "streams":
                return redirect("streams")
            else:
                return redirect("/canal/"+page)

    except Exception as e:
        raise

def login_view(request, page):
    try:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #request.session.set_expiry(30)
            perfil = request.user.perfil
            perfil.status = "online"
            perfil.save()
            if page == "streams" or page == "index":
                return redirect("streams")
            else:
                return redirect("/canal/"+page)
        else:
            if page == "streams" or page == "index":
                return redirect("streams")
            else:
                return redirect("/canal/"+page)
    except Exception as e:
        if page == "streams" or page == "index":
            return redirect("streams")
        else:
            return redirect("/canal/"+page)

def logout_view(request, page):
    try:
        perfil = request.user.perfil
        perfil.status = "offline"
        perfil.assistindo = ""
        perfil.save()
        if Transmissao.objects.filter(streamer=perfil.nome):
            encerraStream(request)
        logout(request)
        if page == "index":
            return redirect("index")
        elif page == "streams":
            return redirect("streams")
        else:
            return redirect("/canal/"+page)
    except Exception as e:
        perfil = request.user.perfil
        perfil.status = "offline"
        perfil.assistindo = ""
        perfil.save()
        logout(request)
        if page == "index":
            return redirect("index")
        elif page == "streams":
            return redirect("streams")
        else:
            return redirect("/canal/"+page)

def iniciaStream(request):
    contAvaliacao = 0
    nota = 0
    try:
        perfil = request.user.perfil
        nome = perfil.nome
        titulo = request.POST['titulo']
        area = request.POST['area']
        imagem = request.FILES["imagem"]
        x = datetime.datetime.now()
        if Avaliacao.objects.filter(avaliado=perfil.id):
            avaliacao = Avaliacao.objects.filter(avaliado=perfil.id)
            for row in avaliacao:
                contAvaliacao += float(row.nota)
            nota = contAvaliacao/len(avaliacao)
            if len(str(nota)) > 3:
                nota = round(nota, 1)
        else:
            nota = 0
        caminho = 'app/static/users/'+nome+'/stream.jpg'
        with open(caminho, 'wb+') as destination:
            for chunk in imagem.chunks():
                destination.write(chunk)
        caminhoBanco = "users/"+nome+"/stream.jpg"
        stream = Transmissao(streamer=nome, titulo=titulo, imagem=caminhoBanco, area=area, hrInicio=x, tempoLive=0, streamer_imagem=perfil.imagem_perfil, views=0, avaliacao=nota)
        stream.save()
        perfil.status = "streaming"
        perfil.save()
        return redirect("/canal/"+nome)
    except Exception as e:
        raise

def encerraStream(request):
    try:
        perfil = request.user.perfil
        stream = Transmissao.objects.get(streamer=perfil.nome)
        perfil_to_modify = Perfil.objects.filter(assistindo=stream.id)
        for row in perfil_to_modify:
            row.assistindo = ""
            row.save()
        stream.delete()
        chat = Chat.objects.filter(streamer_room=perfil.id)
        for c in chat:
            c.delete()
        perfil.status = "online"
        perfil.save()
        return redirect("/painel/"+perfil.nome)
    except Exception as e:
        return redirect("/painel/"+perfil.nome)

def seguir(request):
    data = {}
    seguidores = 0
    if 'streamer' in request.GET:
        try:
            streamer_nome = request.GET.get('streamer', None)
            perfil = request.user.perfil
            nome = perfil.nome
            segue = Segue(seguindo=streamer_nome, seguidor=nome)
            segue.save()
            nSegue = Segue.objects.filter(seguindo=streamer_nome)
            for row in nSegue:
                seguidores = seguidores + 1
            data = {
                'result': True, 'seguidores': seguidores
            }
            return JsonResponse(data)
        except Exception as e:
            data['result'] = False
            return JsonResponse(data)
    else:
        data['result'] = False
        return JsonResponse(data)

def unfollow(request):
    data = {}
    seguidores = 0
    if 'streamer' in request.GET:
        try:
            streamer_nome = request.GET.get('streamer', None)
            perfil = request.user.perfil
            nome = perfil.nome
            streamer = Perfil.objects.get(nome=streamer_nome)
            segue = Segue.objects.filter(seguindo=streamer_nome, seguidor=nome)
            segue.delete()
            nSegue = Segue.objects.filter(seguindo=streamer_nome)
            for row in nSegue:
                seguidores = seguidores + 1
            data = {
                'result': True, 'seguidores': seguidores
            }
            return JsonResponse(data)
        except Exception as e:
            data['result'] = False
            return JsonResponse(data)

def teste(request):
    return render(request, "teste.html", {"perfil_logado": perfil_logado(request), "dados": userDados(request)})

def ajax(request):
    data = {}
    if 'username' in request.GET:
        username = request.GET.get('username', None)
        try:
            perfil = Perfil.objects.get(nome=username)
            if perfil is not None:
                data = {
                    'result': True, 'msg_erro': 'Usuário existente'
                }
        except Exception as e:
            data['result'] = False
        return JsonResponse(data)

    elif 'email' in request.GET:
        email = request.GET.get('email', None)
        try:
            email_exists = User.objects.filter(email=email).exists()
            if email_exists:
                data = {
                    'result': True, 'msg_erro': 'Email sendo utilizado'
                }
        except Exception as e:
            data['result'] = False
        return JsonResponse(data)

def validaCadastro(request):
    data = {}
    if 'username' in request.GET:
        username = request.GET.get('username', None)
        try:
            username_exists = User.objects.filter(username=username).exists()
            if username_exists:
                data = {
                    'result': True
                }
            return JsonResponse(data)
        except Exception as e:
            data['result'] = False
            return JsonResponse(data)
    elif 'email' in request.GET:
        email = request.GET.get('email', None)
        try:
            email_exists = User.objects.filter(email=email).exists()
            if email_exists:
                data = {
                    'result': True
                }
            return JsonResponse(data)
        except Exception as e:
            data['result'] = False
            return JsonResponse(data)

def validaLogin(request):
    data = {}
    if 'username' in request.POST and 'password' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        try:
            user_exists = authenticate(request, username=username, password=password)
            if user_exists is not None:
                data = {
                    'result': True,
                }
            return JsonResponse(data)
        except Exception as e:
            data['result'] = False
            return JsonResponse(data)

def Messages(request, streamer_id):
    c = Chat.objects.filter(streamer_room=streamer_id)
    return render(request, 'messages.html', {'chat': c})

def PostMsg(request, streamer_id):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)
        perfil = request.user.perfil
        nome = perfil.nome
        c = Chat(username=nome, message=msg, streamer_room=streamer_id)
        if msg != '':
            c.save()
        msg = nome+": "+msg
        return JsonResponse({ 'msg': msg, 'user': nome})
    else:
        return HttpResponse('Request must be POST.')

def chat(request, streamer_id):
    stream = None
    perfil = None
    numero_seguidores = 0
    botao_seguir = None
    streamer = Perfil.objects.get(id=streamer_id)
    if perfil_logado(request):
        perfil = request.user.perfil
        botao_seguir = Segue.objects.filter(seguindo=streamer.nome, seguidor=perfil.nome)
    seguidores = Segue.objects.filter(seguindo=streamer.nome)
    for row in seguidores:
        numero_seguidores = numero_seguidores + 1
    c = Chat.objects.filter(streamer_room=streamer_id)
    try:
        stream = Transmissao.objects.get(streamer=streamer.nome)
        return render(request, "chat.html", {"perfil_logado": perfil_logado(request), "streamer": streamer, "stream": stream, "seguidores": numero_seguidores, "botao_seguir": botao_seguir, "chat": c})
    except Exception as e:
        return render(request, "chat.html", {"perfil_logado": perfil_logado(request), "streamer": streamer, "stream": stream, "seguidores": numero_seguidores, "botao_seguir": botao_seguir, "chat": c})

def atualizaFiltro(request):
    area = Area.objects.all()
    nArea = len(area)
    outros = []
    if 'filtro' in request.GET:
        filtro = request.GET.get('filtro', None)
        if filtro == "todas":
            return render(request, "mini.html", {"streams": Transmissao.objects.all(), "area": area, "nArea": nArea})
        else:
            if 'avaliacaoFil' in request.GET:
                avaliacao = request.GET.get('avaliacaoFil', None)
                if avaliacao == "asc":
                    returnFiltro = Transmissao.objects.filter(area=filtro).order_by('avaliacao')
                    return render(request, "mini.html", {"streams": returnFiltro, "area": area, "filtro": filtro, "avaliacao": "Crescente", "idAva": avaliacao})
                else:
                    returnFiltro = Transmissao.objects.filter(area=filtro).order_by('-avaliacao')
                    return render(request, "mini.html", {"streams": returnFiltro, "area": area, "filtro": filtro, "avaliacao": "Crescente", "idAva": avaliacao})
            else:
                returnFiltro = Transmissao.objects.filter(area=filtro)
                return render(request, "mini.html", {"streams": returnFiltro, "area": area, "nArea": nArea, "filtro": filtro})
    elif 'avaliacao' in request.GET:
        avaliacao = request.GET.get('avaliacao', None)
        if avaliacao == "asc":
            if 'filtroAv' in request.GET:
                filtro = request.GET.get('filtroAv', None)
                resultFiltro = Transmissao.objects.filter(area=filtro).order_by('avaliacao')
                return render(request, "mini.html", {"streams": resultFiltro, "area": area, "filtro": filtro, "nArea": nArea, "avaliacao": "Crescente", "idAva": avaliacao})
            else:
                resultFiltro = Transmissao.objects.all().order_by('avaliacao')
                return render(request, "mini.html", {"streams": resultFiltro, "area": area, "nArea": nArea, "avaliacao": "Crescente", "idAva": avaliacao})
        else:
            if 'filtroAv' in request.GET:
                filtro = request.GET.get('filtroAv', None)
                resultFiltro = Transmissao.objects.filter(area=filtro).order_by('-avaliacao')
                return render(request, "mini.html", {"streams": resultFiltro, "area": area, "filtro": filtro, "nArea": nArea, "avaliacao":"Decrescente", "idAva": avaliacao})
            else:
                resultFiltro = Transmissao.objects.all().order_by('-avaliacao')
                return render(request, "mini.html", {"streams": resultFiltro, "area": area, "nArea": nArea, "avaliacao": "Decrescente", "idAva": avaliacao})

def painel(request, streamer_nome):
    if perfil_logado(request):
        perfil = perfil_logado(request)
        if perfil.nome == streamer_nome:
            return render(request, "userpanel.html", {"perfil_logado" : perfil_logado(request), "perfil_status": perfil_status(request)})
        else:
            return redirect("index")
    else:
        return redirect("index")

def userIframe(request):
    stream = None
    perfil = perfil_logado(request)
    if Transmissao.objects.filter(streamer=perfil.nome):
        stream = Transmissao.objects.get(streamer=perfil.nome)
    return render(request, "userIframe.html", {"perfil_logado" : perfil_logado(request), "area": Area.objects.all(), "not_streaming": perfil_status(request), "stream": stream, "seguidores": len(Segue.objects.filter(seguindo=perfil.nome))})

def userTutorial(request):
    stream = None
    perfil = perfil_logado(request)
    return render(request, "userTutorial.html")

def obsS(request):
    stream = None
    perfil = perfil_logado(request)
    return render(request, "obs.html")



def avaliacao(request):
    contAvaliacao = 0
    nota = request.GET.get('nota', None)
    streamer = request.GET.get('streamer', None)
    user = perfil_logado(request)
    if Avaliacao.objects.filter(avaliado=streamer, avaliador=user.id):
        avaliacao = Avaliacao.objects.get(avaliado=streamer, avaliador=user.id)
        avaliacao.nota = nota
        avaliacao.save()
    else:
        a = Avaliacao(nota=nota, avaliado=streamer, avaliador=user.id)
        a.save()

    avaliacoes = Avaliacao.objects.filter(avaliado=streamer)
    for row in avaliacoes:
        contAvaliacao += float(row.nota)
    nota = contAvaliacao/len(avaliacoes)
    if len(str(nota)) > 3:
        nota = round(nota, 1)

    streamer = Perfil.objects.get(id=streamer)
    if Transmissao.objects.filter(streamer=streamer.nome):
        s = Transmissao.objects.get(streamer=streamer.nome)
        s.avaliacao = nota
        s.save()

    data = {
        'result': True, 'nota': nota
    }

    return JsonResponse(data)

def mudaFoto(request):
    nomeImg = ""
    if perfil_logado(request):
        img = request.FILES['userimg']
        perfil = perfil_logado(request)
        caminho = 'app/static/users/'+perfil.nome+'/'+img.name+'.jpg'
        with open(caminho, 'wb+') as destination:
            for chunk in img.chunks():
                destination.write(chunk)
        caminhoBanco = "users/"+perfil.nome+'/'+img.name+'.jpg'
        perfil.imagem_perfil = caminhoBanco
        perfil.save()
        if os.path.isfile(caminho):
            for CleanUp in glob.glob('app/static/users/'+perfil.nome+'/*'):
                print CleanUp
                if not CleanUp.endswith(img.name+'.jpg') and not CleanUp.endswith("stream.jpg"):
                    os.remove(CleanUp)
        if Transmissao.objects.filter(streamer=perfil.nome):
            stream = Transmissao.objects.get(streamer=perfil.nome)
            stream.streamer_imagem = caminhoBanco
            stream.save()
        data = {
            "result": True, "caminho": caminhoBanco
        }
        return JsonResponse(data)

def atualizaDadosStream(request):
    img = None
    area = None
    titulo = None
    perfil = perfil_logado(request)
    if Transmissao.objects.filter(streamer=perfil.nome):
        stream = Transmissao.objects.get(streamer=perfil.nome)
        if 'titulo' in request.POST:
            titulo = request.POST['titulo']
            if titulo != "":
                stream.titulo = titulo
        if 'imagem' in request.FILES:
            img = request.FILES['imagem']
            if img != None:
                caminho = 'app/static/users/'+perfil.nome+'/stream.jpg'
                with open(caminho, 'wb+') as destination:
                    for chunk in img.chunks():
                        destination.write(chunk)
                caminhoBanco = "users/"+perfil.nome+'/stream.jpg'
                stream.imagem = caminhoBanco
        if 'area' in request.POST:
            area = request.POST['area']
            if area != "":
                stream.area = area

        stream.save()
    return redirect("/canal/"+perfil.nome)

def config(request):
    img = None
    seguindo = []
    if "att_img" in request.GET:
        img = request.GET.get('att_img', None)
    stream = None
    perfil = perfil_logado(request)
    if Segue.objects.filter(seguidor=perfil.nome):
        segue = Segue.objects.filter(seguidor=perfil.nome)
        for row in segue:
            perfil = Perfil.objects.get(nome=row.seguindo)
            seguindo.append(perfil)
    return render(request, "config.html", {"perfil_logado": perfil_logado(request), "dados": userDados(request), "img": img, "seguindo": seguindo})

def mudaFotoUser(request):
    perfil = perfil_logado(request)
    img = request.FILES['imagem']
    if img != None:
        caminho = 'app/static/users/'+perfil.nome+'/prev.jpg'
        with open(caminho, 'wb+') as destination:
            for chunk in img.chunks():
                destination.write(chunk)
        caminhoBanco = "users/"+perfil.nome+'/prev.jpg'
        data = {
            "caminho": caminhoBanco
        }
        return JsonResponse(data)
    else:
        return None

def validaAtualizaDadosUser(request):
    data = {
        'result': False
    }
    if 'nome' in request.GET:
        nome = request.GET.get('nome', None)
        if Perfil.objects.filter(nome=nome):
            data['result'] = True
    if 'email' in request.GET:
        email = request.GET.get('email', None)
        if User.objects.filter(email=email):
            data['result'] = True
    if 'senhaAtual' in request.GET:
        senhaAtual = request.GET.get('senhaAtual', None)
        perfil = perfil_logado(request)
        user_exists = authenticate(request, username=perfil.nome, password=senhaAtual)
        if user_exists is None:
            data['result'] = True
    return JsonResponse(data)

def atualizaDadosUser(request):
    imagem = None
    nome = None
    email = None
    senha = None
    perfil = perfil_logado(request)
    user = User.objects.get(username=perfil.nome)
    if 'nome' in request.POST:
        nome = request.POST['nome']
        if nome != "":
            os.rename('app/static/users/'+perfil.nome,'app/static/users/'+nome)
            perfil.nome = nome
            caminhoImg = perfil.imagem_perfil
            caminhoImg = caminhoImg.split('/')
            imgNome = caminhoImg[2]
            if imgNome != "user.png":
                perfil.imagem_perfil = "users/"+nome+"/"+imgNome
            user.username = nome
    if 'imagem' in request.FILES:
        imagem = request.FILES['imagem']
        if imagem != None:
            if nome != None:
                caminho = 'app/static/users/'+nome+'/'+imagem.name+'.jpg'
                caminhoBanco = "users/"+nome+'/'+imagem.name+'.jpg'
            else:
                caminho = 'app/static/users/'+perfil.nome+'/'+imagem.name+'.jpg'
                caminhoBanco = "users/"+perfil.nome+'/'+imagem.name+'.jpg'
            with open(caminho, 'wb+') as destination:
                for chunk in imagem.chunks():
                    destination.write(chunk)
            if os.path.isfile(caminho):
                for CleanUp in glob.glob('app/static/users/'+perfil.nome+'/*'):
                    print CleanUp
                    if not CleanUp.endswith(imagem.name+'.jpg') and not CleanUp.endswith("stream.jpg"):
                        os.remove(CleanUp)
            perfil.imagem_perfil = caminhoBanco
    if 'email' in request.POST:
        email = request.POST['email']
        if email != "":
            user.email = email
    if 'senha' in request.POST:
        senha = request.POST['senha']
        if senha != "":
            user.set_password(senha)
    perfil.save()
    user.save()
    usuario = authenticate(request, username=nome, password=senha)
    login(request, usuario)

    return redirect("/painel/"+perfil.nome)
