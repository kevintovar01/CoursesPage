from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from registra.models import Registra
from .serializers import RegistraSerializer
from users.models import Role
from users.api.serializers import RoleSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions, viewsets

class IsAdminRole(permissions.BasePermission):
    """
    Permiso para permitir solo a administradores acceder a la vista.
    """
    message = "You need admin privileges to perform this action."

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return user.roles.filter(name__iexact='admin').exists()

class RegistraList(APIView):
    """
    Maneja GET (listar todos) y POST (crear)
    Solo accesible para administradores
    """
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get(self, request):
        registros = Registra.objects.all()
        serializer = RegistraSerializer(registros, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RegistraSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegistraDetail(APIView):
    """
    Maneja GET (detalle), PUT (actualizar) y DELETE
    Solo accesible para administradores
    """
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get_object(self, pk):
        try:
            return Registra.objects.get(pk=pk)
        except Registra.DoesNotExist:
            return None

    def get(self, request, pk):
        registro = self.get_object(pk)
        if registro:
            serializer = RegistraSerializer(registro)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        registro = self.get_object(pk)
        if registro:
            serializer = RegistraSerializer(registro, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        registro = self.get_object(pk)
        if registro:
            registro.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

class RoleViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Role
    Solo accesible para administradores
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]