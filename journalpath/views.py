# -*- coding: utf-8 -*-

from datetime import datetime

from django.shortcuts import render
from django.contrib import auth, messages
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import connection

from .models import *


def dictfetchall(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def index(request):
    context = {'active': 'home'}
    if not request.user.is_authenticated:
        messages.error(request, 'You need to login')
        return HttpResponseRedirect(reverse('login'))
    return render(request, 'journalpath/index.html', context)


def login(request):
    # Definiendo la funcion iniciar sesion con un requerimiento POST
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Usamos el metodo de autenticar de django para validar la informacion
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Contraseña correcta, se marca el usuario como activo
            auth.login(request, user)
            messages.success(request, 'Login sucessfully')
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, 'Autentication error, please check your credentials')
            return HttpResponseRedirect(reverse('login'))
    else:
        # Si no es un request tipo POST se renderiza el login
        return render(request, 'journalpath/login.html')


def logout(request):
    # Cerrando sesion
    auth.logout(request)
    messages.success(request, 'Session is closed')
    return HttpResponseRedirect(reverse('login'))


def catalog_list(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You need to login')
        return HttpResponseRedirect(reverse('login'))
    try:
        user_catalog = Catalog.objects.filter(user_id=request.user).order_by('-date')
    except models.ObjectDoesNotExist:
        user_catalog = False

    page = request.GET.get('page', 1)
    paginator = Paginator(user_catalog, 20)
    try:
        catalog_data = paginator.page(page)
    except PageNotAnInteger:
        catalog_data = paginator.page(1)
    except EmptyPage:
        catalog_data = paginator.page(paginator.num_pages)

    context = {
        'active': 'catalog',
        'catalog_data': catalog_data,
    }

    return render(request, 'journalpath/catalog_list.html', context)


def session_list(request):

    if not request.user.is_authenticated:
        messages.error(request, 'You need to login')
        return HttpResponseRedirect(reverse('login'))

    try:
        user_sessions = Session.objects.filter(user_id=request.user).order_by('-id')
    except models.ObjectDoesNotExist:
        user_sessions = False

    page = request.GET.get('page', 1)
    paginator = Paginator(user_sessions, 20)
    try:
        session_data = paginator.page(page)
    except PageNotAnInteger:
        session_data = paginator.page(1)
    except EmptyPage:
        session_data = paginator.page(paginator.num_pages)

    context = {
        'active': 'sessions',
        'session_data': session_data,
    }
    return render(request, 'journalpath/session_list.html', context)


def catalog_form(request, catalog_id):

    if not request.user.is_authenticated:
        messages.error(request, 'You need to login')
        return HttpResponseRedirect(reverse('login'))
    authors = Author.objects.all().order_by('name')
    try:
        catalog_id = Catalog.objects.get(id=catalog_id)
    except models.ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('catalog_list'))

    if request.method == 'POST':
        if request.POST['submit'] == 'delete_item':
            catalog_id.delete()

            return HttpResponseRedirect(reverse('catalog_list'))
        if request.POST['submit'] == 'cancel':
            return HttpResponseRedirect(reverse('catalog_list'))

        if request.POST['submit'] == 'save_item':
            catalog_id.name = request.POST['name']
            catalog_id.date = datetime.strptime(request.POST['date'], "%Y-%m-%d")
            catalog_id.author = Author.objects.get(id=request.POST['author'])
            catalog_id.type = request.POST['type']
            catalog_id.difficulty = request.POST['difficulty']
            catalog_id.self_appraisal = request.POST['self_appraisal']
            catalog_id.note = request.POST['note']
            catalog_id.save()

    # Statics
    with connection.cursor() as cursor:
        cursor.execute("SELECT sum(duration), count(id) from journalpath_session "
                       "WHERE catalog_id={catalog} ".format(catalog=catalog_id.id))
        practiced = cursor.fetchall()
    with connection.cursor() as cursor:
        cursor.execute("SELECT sum(duration), count(id) from journalpath_session "
                       "WHERE catalog_id={catalog} "
                       "AND date > '2018-08-12'".format(catalog=catalog_id.id))
        practiced_lw = cursor.fetchall()
    context = {
        'active': 'catalog',
        'catalog_id': catalog_id,
        'authors': authors,
        'practiced_time': practiced[0][0],
        'practiced_times': practiced[0][1],
        'practiced_time_lw': practiced_lw[0][0],
        'practiced_times_lw': practiced_lw[0][1],
    }

    return render(request, 'journalpath/catalog_form.html', context)


def catalog_new(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You need to login')
        return HttpResponseRedirect(reverse('lolpath:login'))
    authors = Author.objects.all().order_by('name')

    context = {
        'active': 'catalog',
        'catalog_id': False,
        'authors': authors,
    }
    if request.method == 'POST':
        if request.POST['submit'] == 'submit_item' or request.POST['submit'] == 'submit_new':
            # Agregando reg
            author_req = request.POST['author']
            author = Author.objects.get(id=author_req)

            new_piece = Catalog(
                name=request.POST['name'],
                author=author,
                type=request.POST['type'],
                date=datetime.strptime(request.POST['date'], "%Y-%m-%d"),
                difficulty=request.POST['difficulty'],
                self_appraisal=request.POST['self_appraisal'],
                note=request.POST['note'],
                user=request.user,
            )
            new_piece.save()
            messages.success(request, 'Piece registered successfully')
            return HttpResponseRedirect(reverse('catalog_list'))

        if request.POST['submit'] == 'cancel':
            return HttpResponseRedirect(reverse('catalog_list'))
    return render(request, 'journalpath/catalog_form.html', context)


def session_new(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You need to login')
        return HttpResponseRedirect(reverse('lolpath:login'))
    catalogs = Catalog.objects.all().order_by('name')

    context = {
        'active': 'sessions',
        'session_id': False,
        'catalogs': catalogs,
    }
    if request.method == 'POST':
        if request.POST['submit'] == 'submit_item':
            # Agregando reg
            catalog_req = request.POST['catalog']
            catalog = Catalog.objects.get(id=catalog_req)
            catalog_type = catalog.type

            new_piece = Session(
                catalog=catalog,
                date=datetime.strptime(request.POST['date'], "%Y-%m-%d"),
                type=catalog_type,
                rate=request.POST['rate'] or 0,
                tempo=request.POST['tempo'] or 0,
                emoji=request.POST['emoji'],
                detail=request.POST['detail'],
                unit=request.POST['unit'],
                duration=request.POST['duration'] or 0,
                user=request.user,
            )
            new_piece.save()
            messages.success(request, 'Session registered successfully')
            return HttpResponseRedirect(reverse('session_list'))

        if request.POST['submit'] == 'cancel':
            return HttpResponseRedirect(reverse('session_list'))
    return render(request, 'journalpath/session_form.html', context)


def session_form(request, session_id):

    if not request.user.is_authenticated:
        messages.error(request, 'You need to login')
        return HttpResponseRedirect(reverse('login'))
    try:
        session_id = Session.objects.get(id=session_id)
    except models.ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('catalog_list'))
    catalogs = Catalog.objects.all().order_by('name')
    if request.method == 'POST':
        if request.POST['submit'] == 'delete_item':
            session_id.delete()
            return HttpResponseRedirect(reverse('session_list'))
        if request.POST['submit'] == 'cancel':
            return HttpResponseRedirect(reverse('session_list'))

    context = {
        'active': 'sessions',
        'session_id': session_id,
        'catalogs': catalogs,
    }

    return render(request, 'journalpath/session_form.html', context)