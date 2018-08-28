from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('catalog_list', views.catalog_list, name='catalog_list'),
    path('session_list', views.session_list, name='session_list'),
]
