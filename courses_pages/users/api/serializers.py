#Django rest framework
from rest_framework import serializers
from ..models import Role, User, Country

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'born_date', 'country', 'password', 'password2')
        extra_kwargs = {'password': {'write_only': True}}

    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email', 'first_name', 'last_name', 'born_date', 'country')
        extra_kwargs = {'password': {'write_only': True}}

