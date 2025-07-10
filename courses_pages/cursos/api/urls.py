from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CursoViewSet, 
    ModuloViewSet, MaterialViewSet, RealizaViewSet, AdquiereViewSet, 
)

router = DefaultRouter()
router.register(r'cursos', CursoViewSet, basename='cursos')
router.register(r'modulos', ModuloViewSet, basename='modulos')
router.register(r'materiales', MaterialViewSet, basename='materiales')
router.register(r'realiza', RealizaViewSet, basename='realiza')
router.register(r'adquiere', AdquiereViewSet, basename='adquiere')
#router.register(r'recursos', CursoViewSet, basename='recursos')

urlpatterns = [
    path('', include(router.urls)),

]
