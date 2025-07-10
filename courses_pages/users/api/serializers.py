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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email', 'first_name', 'last_name', 'born_date', 'country', 'password')
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            # 1) Extraemos el password plano
            raw_pw = validated_data.pop('password')
            # 2) Creamos el usuario sin el password
            user = User.objects.create(**validated_data)
            # 3) Le hacemos hashing al password y lo guardamos
            user.set_password(raw_pw)
            user.save()
            return user

