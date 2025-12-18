from django.urls import path
from . import views

urlpatterns = [
    path('', views.ConstaDeListCreate.as_view(), name='constade-list'),
    path('<int:pk>/', views.ConstaDeRetrieveUpdateDestroy.as_view(), name='constade-detail'),
]