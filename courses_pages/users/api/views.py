# Django rest framework
from rest_framework import status,permissions,viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView


#models
from ..models import Role, Country, User
#serializers
from .serializers import RoleSerializer, CountrySerializer, UserSerializer

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

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
            for POST we use allowAny; for the other things we use IsAuthenticated.
        """

        if self.action == 'create':
            perms = [permissions.AllowAny]
        elif self.action in ['list', 'retrieve', 'update', 'partial_update', 'destroy']:
            perms = [permissions.IsAuthenticated, IsOwner]
        else:
            perms = [permissions.IsAuthenticated, IsAdminRole]

        return [perm() for perm in perms]
