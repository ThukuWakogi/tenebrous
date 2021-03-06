from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.response import Response
from .models import Image

class UserSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'username', 'email', 'password']
    extra_kwargs = {
      'password': {
        'write_only': True,
        'required': True
      },
      'email': {
        'required': True
      }
    }
  
  def create(self, validated_data):
    user = User.objects.create_user(**validated_data)
    return user

class ImageSerializer(serializers.ModelSerializer):
  class Meta:
    model = Image
    fields = ['id', 'image', 'caption', 'user']
