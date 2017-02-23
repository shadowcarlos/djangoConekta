from django.conf.urls import url, include
from django.contrib import admin
from . import views
urlpatterns = [
    url(r'^cobrar2$', views.cobrar2, name='cobrar2'),
    url(r'^$', views.venta, name='venta'),
    url(r'^cobrar$', views.cobrar, name='cobrar'),
    url(r'^tarjeta$', views.tarjeta, name='tarjeta'),
]