from rest_framework import generics
from constade.models import ConstaDe
from .serializers import ConstaDeSerializer

class ConstaDeListCreate(generics.ListCreateAPIView):
    queryset = ConstaDe.objects.all()
    serializer_class = ConstaDeSerializer

class ConstaDeRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = ConstaDe.objects.all()
    serializer_class = ConstaDeSerializer