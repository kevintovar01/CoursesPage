# Django rest framework
from rest_framework import status,permissions,viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework.decorators import action
#models
from ..models import Role, Country, User
#serializers
from .serializers import RoleSerializer, CountrySerializer, UserSerializer, RegistrationSerializer

class IsAdminRole(permissions.BasePermission):
    """
        Permission to only allow admins to access the view.
    """

    message = "You need a higher level of permission."

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        return user.roles.filter(name__iexact='admin').exists()


class MyLoginView(LoginView):
    template_name = 'rest_framework/login.html'
    redirect_authenticated_user = True
    # si quieres forzar siempre esta página al loguearte:
    next_page = '/api/users/'

class MyLogoutView(LogoutView):
    # Ignoramos cualquier ?next=…
    redirect_field_name = None  
    # Y forzamos este redirect:
    next_page = '/api-auth/login/'


class IsOwner(permissions.BasePermission):
    """
        This allow to the user to edit their own profile.
    """

    message = "you just can edit your own profile."

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

    def get_permissions(self):
        # Permitir que cualquiera se registre...
        if self.action == 'create':
            return [permissions.AllowAny()]
        # ...pero para retrieve, debe estar autenticado
        return [permissions.IsAuthenticated()]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        # get  /api/users/me/
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def get_permissions(self):
        """
            for POST we use allowAny; for the other things we use IsAuthenticated.
        """

        if self.action in ['list', 'retrieve', 'update', 'partial_update', 'destroy']:
            perms = [permissions.IsAuthenticated]
            if self.action in ['list', 'retrieve']:
                perms = [permissions.IsAuthenticated, IsAdminRole]
            if self.action in ['update', 'partial_update', 'destroy']:
                perms = [permissions.IsAuthenticated, IsOwner]
        else:
            perms = [permissions.IsAuthenticated]

        return [perm() for perm in perms]


