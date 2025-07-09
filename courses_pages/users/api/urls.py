# Django

from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

#views
from .views import RoleViewSet

router = DefaultRouter()
router.register(r'roles', RoleViewSet, basename='role')

urlpatterns = [
    path('', include(router.urls)),
]

