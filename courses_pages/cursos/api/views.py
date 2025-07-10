from django.shortcuts import render
from django.db.models import Count, Avg
from django.db import connection
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Curso, Modulo, Material, Realiza, Adquiere
from .serializers import CursoSerializer, ModuloSerializer, MaterialSerializer, RealizaSerializer, AdquiereSerializer

# Create your views here.

class IsEstudiante(permissions.BasePermission):
    """
    Permiso personalizado para permitir solo a usuarios con rol 'Estudiante'.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and hasattr(request.user, 'rol') and request.user.rol == 'Estudiante'

# Usando APIView para control total sobre el modelo Curso
class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

    @action(detail=False, methods=['get'])
    def estudiantes_matriculados(self, request):
        """
        2. Estudiantes matriculados por curso
        """
        cursos = Curso.objects.annotate(
            estudiantesMatriculados=Count('adquiere'),
            progresoPromedio=Avg('adquiere__porcAvance')
        ).order_by('-estudiantesMatriculados')
        
        data = [{
            'nombreCurso': curso.nombreCurso,
            'nivelCurso': curso.nivelCurso,
            'estudiantesMatriculados': curso.estudiantesMatriculados,
            'progresoPromedio': round(curso.progresoPromedio, 2) if curso.progresoPromedio else 0
        } for curso in cursos]
        
        return Response(data)

    @action(detail=True, methods=['get'])
    def recursos(self, request, pk=None):
        """
        3. Uso de recursos por curso
        """
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT mo.nombreModulo, COUNT(ma.idMaterial) AS totalMateriales, STRING_AGG(ma.tipo, ', ') AS tiposMateriales
                FROM cursos_modulo mo
                INNER JOIN cursos_contiene co ON mo.idModulo = co.idModulo
                INNER JOIN cursos_material ma ON co.idMaterial = ma.idMaterial
                WHERE mo.idCurso_id = %s
                GROUP BY mo.idModulo, mo.nombreModulo
                ORDER BY mo.nombreModulo;
            """, [pk])
            rows = cursor.fetchall()

        data = [{
            'nombreModulo': row[0],
            'totalMateriales': row[1],
            'tiposMateriales': row[2]
        } for row in rows]
        
        return Response(data)

    @action(detail=False, methods=['get'], permission_classes=[IsEstudiante])
    def cursos_no_adquiridos(self, request):
        """
        12. Cursos disponibles para inscribirse (que no he adquirido)
        """
        cursos = Curso.objects.exclude(adquiere__usuario=request.user).annotate(
            calificacionPromedio=Avg('reseña__valorCalificacion')
        ).order_by('-calificacionPromedio')

        serializer = self.get_serializer(cursos, many=True)
        return Response(serializer.data)


class ModuloViewSet(viewsets.ModelViewSet):
    queryset = Modulo.objects.all()
    serializer_class = ModuloSerializer

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

class RealizaViewSet(viewsets.ModelViewSet):
    queryset = Realiza.objects.all()
    serializer_class = RealizaSerializer

class AdquiereViewSet(viewsets.ModelViewSet):
    queryset = Adquiere.objects.all()
    serializer_class = AdquiereSerializer
    permission_classes = [IsEstudiante]
