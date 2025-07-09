# api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Si usas APIView
    path('categorias/', views.CategoriaList.as_view(), name='categoria-list'),
    path('categorias/<int:pk>/', views.CategoriaDetail.as_view(), name='categoria-detail'),
    
    # O si usas vistas genéricas
    # path('categorias/', views.CategoriaListCreate.as_view(), name='categoria-list'),
    # path('categorias/<int:pk>/', views.CategoriaRetrieveUpdateDestroy.as_view(), name='categoria-detail'),
]