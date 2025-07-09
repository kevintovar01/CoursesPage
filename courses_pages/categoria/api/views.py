# api/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from categoria.models import Categoria
from .serializers import CategoriaSerializer

# Opción 1: Usando APIView para control total
class CategoriaList(APIView):
    def get(self, request):
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoriaDetail(APIView):
    def get_object(self, pk):
        try:
            return Categoria.objects.get(pk=pk)
        except Categoria.DoesNotExist:
            return None
    
    def get(self, request, pk):
        categoria = self.get_object(pk)
        if categoria is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CategoriaSerializer(categoria)
        return Response(serializer.data)
    
    def put(self, request, pk):
        categoria = self.get_object(pk)
        if categoria is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CategoriaSerializer(categoria, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        categoria = self.get_object(pk)
        if categoria is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        categoria.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Opción 2: Usando vistas genéricas (más conciso)
class CategoriaListCreate(ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class CategoriaRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer