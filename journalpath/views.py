from django.shortcuts import render
from django.contrib import auth, messages
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
        user_catalog = Catalog.objects.filter(user_id=request.user).order_by('-id')
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

