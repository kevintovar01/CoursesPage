from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CursoList, CursoDetail, 
    ModuloViewSet, MaterialViewSet, RealizaViewSet
)

router = DefaultRouter()
router.register(r'modulos', ModuloViewSet)
router.register(r'materiales', MaterialViewSet)
router.register(r'realiza', RealizaViewSet)

urlpatterns = [
    path('cursos/', CursoList.as_view(), name='curso-list'),
    path('cursos/<int:pk>/', CursoDetail.as_view(), name='curso-detail'),
    path('', include(router.urls)),
]
