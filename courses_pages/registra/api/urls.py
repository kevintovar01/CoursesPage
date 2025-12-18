from django.urls import path
from . import views

urlpatterns = [
    path('', views.RegistraList.as_view(), name='registra-list'),
    path('<int:pk>/', views.RegistraDetail.as_view(), name='registra-detail'),
]