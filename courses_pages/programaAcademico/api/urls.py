# api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Si usas APIView
    path('programaAcademicos/', views.programaAcademicoList.as_view(), name='programaAcademico-list'),
    path('programaAcademicos/<int:pk>/', views.programaAcademicoDetail.as_view(), name='programaAcademico-detail'),
    
    # O si usas vistas genéricas
    # path('programaAcademicos/', views.programaAcademicoListCreate.as_view(), name='programaAcademico-list'),
    # path('programaAcademicos/<int:pk>/', views.programaAcademicoRetrieveUpdateDestroy.as_view(), name='programaAcademico-detail'),
]