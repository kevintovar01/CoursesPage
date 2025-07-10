# Django

from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token


#views
from .views import RoleViewSet, CountryViewSet, UserViewSet, RegistrationViewSet, MyLoginView, MyLogoutView

router = DefaultRouter()
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'countries', CountryViewSet, basename='country')
router.register(r'users', UserViewSet, basename='user')

router.register(r'registration', RegistrationViewSet, basename='registration')

signup_router = DefaultRouter()
signup_router.register(r'registration', RegistrationViewSet, basename='registration')
urlpatterns = [
    path('', include(router.urls), name='roles'),
    path('', include(router.urls), name='login'),
    path('', include(router.urls), name='users'),
    path('signup/', include(signup_router.urls), name='signup'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
]

