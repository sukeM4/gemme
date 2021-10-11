from rest_framework import serializers
from myapp.models import Item
# from lilo
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['description', 'img']



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['is_active']


class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['user'] = UserSerializer(self.user).data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class RegisterSerializer(UserSerializer):
    password = serializers.CharField(
        max_length=128, min_length=8, write_only=True, required=True)
    email = serializers.EmailField(
        required=True, write_only=True, max_length=128)

    class Meta:
        model = User
        # fields = ['id', 'username', 'email', 'password', 'is_active', 'created', 'updated']
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        # try:
        #     user = User.objects.get(email=validated_data['email'])
        # except ObjectDoesNotExist:
        #     user = User.objects.create_user(**validated_data, is_active=True)
        
        user = User.objects.create_user(**validated_data, is_active=True)
        # user.is_active = False
        # user.save()

        return user

