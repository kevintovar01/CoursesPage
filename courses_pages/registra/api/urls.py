from django.urls import path
from . import views

urlpatterns = [
    path('registros/', views.RegistraList.as_view(), name='registra-list'),
    path('registros/<int:pk>/', views.RegistraDetail.as_view(), name='registra-detail'),
]