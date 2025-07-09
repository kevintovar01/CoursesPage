from django.urls import path
from . import views

urlpatterns = [
    path('constade/', views.ConstaDeListCreate.as_view(), name='constade-list'),
    path('constade/<int:pk>/', views.ConstaDeRetrieveUpdateDestroy.as_view(), name='constade-detail'),
]