from django.shortcuts import render
from django.db.models import Count, Avg
from django.db import connection
from rest_framework import viewsets, status, permissions, serializers
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Curso, Modulo, Material, Realiza, Adquiere, settings
from .serializers import (
    CursoSerializer,
    ModuloSerializer,
    MaterialSerializer,
    RealizaSerializer,
    AdquiereSerializer
)

# Create your views here.

class IsEstudiante(permissions.BasePermission):
    """
    Permiso para permitir solo a usuarios con rol 'Estudiante' acceder a la vista.
    """
    message = "Solo los usuarios con el rol de Estudiante pueden realizar esta acción."

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        # Asumiendo que el modelo User tiene un campo 'rol' de tipo CharField.
        #print(user.roles.filter(name__iexact='estudiante').exists())
        
        return user.roles.filter(name__iexact='estudiante').exists()
    
class IsDocente(permissions.BasePermission):
    """
    Permiso para permitir solo a usuarios con rol 'Docente' acceder a la vista.
    """
    message = "Solo los usuarios con el rol de Docente pueden realizar esta acción."

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        return user.roles.filter(name__iexact='teacher').exists()

class IsAdmin(permissions.BasePermission):
    """
    Permiso para permitir solo a usuarios con rol 'Admin' o que sean staff.
    """
    message = "Necesitas permisos de Administrador para realizar esta acción."

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False
            
        is_admin_role = user.roles.filter(name__iexact='admin').exists()
        return is_admin_role or user.is_staff

class IsDocenteOrAdmin(permissions.BasePermission):
    """
    Permiso para permitir acceso a usuarios con rol 'Docente' o 'Admin'.
    """
    message = "Solo los usuarios con el rol de profesor o Admin pueden realizar esta acción."

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False
            
        is_docente = user.roles.filter(name__iexact='teacher').exists()
        is_admin = user.roles.filter(name__iexact='admin').exists()
        print(is_docente, is_admin, user.is_staff)
        return is_docente or is_admin or user.is_staff

# Serializer para la vista de estudiantes matriculados
class EstudianteMatriculadoSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='usuario.id')
    email = serializers.EmailField(source='usuario.email')
    first_name = serializers.CharField(source='usuario.first_name')
    last_name = serializers.CharField(source='usuario.last_name')
    porcAvance = serializers.DecimalField(max_digits=5, decimal_places=2)

# Usando APIView para control total sobre el modelo Curso
class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

    @action(detail=True, methods=['get'], permission_classes=[IsDocenteOrAdmin])
    def estudiantes_matriculados(self, request, pk=None):
        """
        2. Estudiantes matriculados en un curso específico.
        Accesible solo para Docentes y Admins.
        """
        try:
            curso = self.get_object()
            adquisiciones = Adquiere.objects.filter(curso=curso).select_related('usuario')
            serializer = EstudianteMatriculadoSerializer(adquisiciones, many=True)
            return Response(serializer.data)
        except Curso.DoesNotExist:
            return Response({"error": "El curso no existe."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'])
    def recursos(self, request, pk=None):
        """
        3. Uso de recursos por curso
        """
        try:
            curso = self.get_object()
            modulos = Modulo.objects.filter(curso=curso).annotate(
                total_materiales=Count('materiales')
            ).prefetch_related('materiales')

            data = []
            for modulo in modulos:
                tipos_materiales = list(modulo.materiales.values_list('tipo', flat=True).distinct())
                data.append({
                    'nombreModulo': modulo.nombreModulo,
                    'totalMateriales': modulo.total_materiales,
                    'tiposMateriales': ', '.join(tipos_materiales) if tipos_materiales else 'Sin materiales'
                })
            
            return Response(data)
        except Curso.DoesNotExist:
            return Response({"error": "El curso no existe."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], permission_classes=[IsEstudiante])
    def cursos_no_adquiridos(self, request):
        """
        12. Cursos disponibles para inscribirse (que no he adquirido)
        """
        # Obtener IDs de cursos que el usuario ya ha adquirido
        cursos_adquiridos_ids = Adquiere.objects.filter(
            usuario=request.user
        ).values_list('curso_id', flat=True)
        
        # Excluir esos cursos de todos los cursos disponibles
        cursos = Curso.objects.exclude(id__in=cursos_adquiridos_ids)
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

    def get_queryset(self):
        """
        Filtra los cursos adquiridos por el usuario autenticado.
        """
        return Adquiere.objects.filter(usuario=self.request.user).select_related('curso', 'usuario')

    @action(detail=False, methods=['get'])
    def mis_cursos(self, request):
        """
        Obtiene los cursos que el usuario ha adquirido con información detallada.
        """
        adquisiciones = self.get_queryset()
        data = []
        for adquisicion in adquisiciones:
            data.append({
                'id': adquisicion.id,
                'curso': {
                    'id': adquisicion.curso.id,
                    'nombreCurso': adquisicion.curso.nombreCurso,
                    'descripcionCurso': adquisicion.curso.descripcionCurso,
                    'nivelCurso': adquisicion.curso.nivelCurso,
                    'precioCurso': str(adquisicion.curso.precioCurso)
                },
                'fechaInicio': adquisicion.fechaInicio,
                'fechaFinalizacion': adquisicion.fechaFinalizacion,
                'porcAvance': str(adquisicion.porcAvance)
            })
        return Response(data)
