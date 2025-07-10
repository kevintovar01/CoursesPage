from rest_framework import generics
from reseña.models import Reseña
from .serializers import ReseñaSerializer
from rest_framework.permissions import IsAuthenticated

class ReseñaList(generics.ListCreateAPIView):
    queryset = Reseña.objects.all()
    serializer_class = ReseñaSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

class ReseñaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reseña.objects.all()
    serializer_class = ReseñaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reseña.objects.filter(usuario=self.request.user)