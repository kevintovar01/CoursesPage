from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CursoViewSet, 
    ModuloViewSet, MaterialViewSet, RealizaViewSet, AdquiereViewSet
)

router = DefaultRouter()
router.register(r'cursos', CursoViewSet)
router.register(r'modulos', ModuloViewSet)
router.register(r'materiales', MaterialViewSet)
router.register(r'realiza', RealizaViewSet)
router.register(r'adquiere', AdquiereViewSet)
router.register(r'recursos', CursoViewSet, basename='recursos')

urlpatterns = [
    path('', include(router.urls)),
]
