from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('catalog_list', views.catalog_list, name='catalog_list'),
    path('catalog_new', views.catalog_new, name='catalog_new'),
    path('catalog_form/<int:catalog_id>', views.catalog_form, name='catalog_form'),
    path('session_list', views.session_list, name='session_list'),
    path('session_new', views.session_new, name='session_new'),
    path('session_form/<int:session_id>', views.session_form, name='session_form'),
]
