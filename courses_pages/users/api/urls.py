# Django

from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

#views
from .views import RoleViewSet, CountryViewSet

router = DefaultRouter()
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'countries', CountryViewSet, basename='country')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(router.urls))
]

