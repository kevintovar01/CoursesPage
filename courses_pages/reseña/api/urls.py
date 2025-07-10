from django.urls import path
from .views import ReseñaList, ReseñaDetail  # Asegúrate de importar correctamente

urlpatterns = [
    path('reseñas/', ReseñaList.as_view(), name='reseña-list'),
    path('reseñas/<int:pk>/', ReseñaDetail.as_view(), name='reseña-detail'),
]