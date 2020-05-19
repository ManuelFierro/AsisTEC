"""KeyNCheck URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Asistencia.views import listado_alumnos,resumen_dia,resumen,datos,index,logindocente,loginalumno

urlpatterns = [
    path('admin/', admin.site.urls,name="adm"),
    path('', index,name="index"), #index primer pantalla, pantalla docente
    path('lista/', listado_alumnos,name="lista"),#listado de alumnos 
    path('resumen_dia/', resumen_dia,name="resumen_dia"),#ResumenDia
    path('resumen/', resumen,name="resumen"),#ResumenTotal
    path('datos/', datos,name="datos"),# RECIBE DATOS DEL QR Y LOS PROCESA
    path('logindocente/', logindocente,name="logindocente"),#PRUEBAS LOGINDOCENTE loginalumno
    path('loginalumno/', loginalumno,name="loginalumno"),
]
