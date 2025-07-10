"""
URL configuration for courses_pages project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
# courses_pages/urls.py (o el nombre de tu proyecto)
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.api.urls')),  # Tus rutas API
    path('api/cursos/', include('cursos.api.urls')), # Ruta para la app cursos
    path('api/categorias/', include('categoria.api.urls')),  # Tus rutas API
    path('api/programaAcademico/', include('programaAcademico.api.urls')),  # Tus rutas API
    path('api/registra/', include('registra.api.urls')),  # Tus rutas API
    path('api/constade/', include('constade.api.urls')),  # Tus rutas API
    path('api-auth/', include('rest_framework.urls')),  
    

    #path('admin/', admin.site.urls),
]
