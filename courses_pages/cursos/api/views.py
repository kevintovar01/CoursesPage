from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Curso, Modulo, Material, Realiza
from .serializers import CursoSerializer, ModuloSerializer, MaterialSerializer, RealizaSerializer

# Create your views here.

# Usando APIView para control total sobre el modelo Curso
class CursoList(APIView):
    def get(self, request):
        cursos = Curso.objects.all()
        serializer = CursoSerializer(cursos, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CursoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CursoDetail(APIView):
    def get_object(self, pk):
        try:
            return Curso.objects.get(pk=pk)
        except Curso.DoesNotExist:
            return None
    
    def get(self, request, pk):
        curso = self.get_object(pk)
        if curso is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CursoSerializer(curso)
        return Response(serializer.data)
    
    def put(self, request, pk):
        curso = self.get_object(pk)
        if curso is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CursoSerializer(curso, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        curso = self.get_object(pk)
        if curso is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        curso.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ModuloViewSet(viewsets.ModelViewSet):
    queryset = Modulo.objects.all()
    serializer_class = ModuloSerializer

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

class RealizaViewSet(viewsets.ModelViewSet):
    queryset = Realiza.objects.all()
    serializer_class = RealizaSerializer
