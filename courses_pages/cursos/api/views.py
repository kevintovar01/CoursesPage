from django.shortcuts import render
from rest_framework import viewsets
from ..models import Curso, Modulo, Material, Realiza
from .serializers import CursoSerializer, ModuloSerializer, MaterialSerializer, RealizaSerializer

# Create your views here.

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

class ModuloViewSet(viewsets.ModelViewSet):
    queryset = Modulo.objects.all()
    serializer_class = ModuloSerializer

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

class RealizaViewSet(viewsets.ModelViewSet):
    queryset = Realiza.objects.all()
    serializer_class = RealizaSerializer
