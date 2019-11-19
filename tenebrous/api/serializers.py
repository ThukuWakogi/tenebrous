from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token 
from rest_framework.response import Response

class UserSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'username', 'email', 'password']
    extra_kwargs = {
      'password': {
        'write_only': True,
        'required': True
      }
    }
  
  def create(self, validated_data):
    user = User.objects.create_user(**validated_data)
    token = Token.objects.create(user=user)
    return Response({ 'token': token.key })
