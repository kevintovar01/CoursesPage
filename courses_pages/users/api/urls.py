# Django

from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

#views
from .views import RoleViewSet, CountryViewSet, UserViewSet

router = DefaultRouter()
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'countries', CountryViewSet, basename='country')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls), name='roles'),
    path('', include(router.urls), name='login'),
    path('', include(router.urls), name='users'),
    path('login/', obtain_auth_token, name='login'),
]

