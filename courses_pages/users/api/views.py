# Django rest framework
from rest_framework import status,permissions,viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView


#models
from ..models import Role
#serializers
from .serializers import RoleSerializer

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

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]