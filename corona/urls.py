"""corona URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from core.views import *
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',signin,name='signin'),
    path('patients/',patients,name='patients'),
    path('doctors/',doctors,name='doctors'),
    path('tests/',tests,name='tests'),
    path('drugs/',drugs,name='drugs'),
    path('blank/',blank,name='blank'),
    path('logout/',logout,name='logout'),
    path('profile/',profile,name='profile'),
    path('orders/',orders,name='orders'),
    path('mails/',mail,name='mail'),
    path('work-schedule/',work_schedule,name='work_schedule'),






]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
