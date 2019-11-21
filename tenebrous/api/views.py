from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from .serializers import UserSerializer, ImageSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.forms.models import model_to_dict
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import RetrieveAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Image

class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def create(self, request, *args,**kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)
    headers = self.get_success_headers(serializer.data)
    token, created = Token.objects.get_or_create(user=serializer.instance)

    return Response(
      {
        'token': token.key,
        'user': serializer.data
      },
      status=status.HTTP_201_CREATED,
      headers=headers
    )

class ObtainAuthTokenAndUserDetails(ObtainAuthToken):
  def post(self, request, *args, **kwargs):
    response = super(ObtainAuthTokenAndUserDetails, self).post(request, *args, **kwargs)
    token = Token.objects.get(key=response.data['token'])
    user = User.objects.get(id=token.user_id)

    return Response({
      'token': token.key,
      'user': {
        'id': user.id,
        'username': user.username,
        'email': user.email
      }
    })

class UserView(RetrieveAPIView):
  queryset = User.objects.all()
  model = User
  serializer_class = UserSerializer
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)

  def retrieve(self, request):
    print(request.user.id)
    return Response({
      'user': {
        'id': request.user.id,
        'username': request.user.username,
        'email': request.user.email
      }
    })

class ImageViewSet(viewsets.ModelViewSet):
  queryset = Image.objects.all()
  serializer_class = ImageSerializer
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticatedOrReadOnly,)

  def list(self, request, *args, **kwargs):
    images = Image.objects.all().order_by('-id')
    serializer = ImageSerializer(images, many=True)
    images_and_users = []

    for pod in serializer.data:
      user = User.objects.get(id=dict(pod)['user'])
      images_and_users.append({
        'id': dict(pod)['id'],
        'caption': dict(pod)['caption'],
        'imageUrl': dict(pod)['image'],
        'user': {
          'id': user.id,
          'username': user.username,
          'email': user.email
        }
      })

    print(images_and_users)

    return Response(images_and_users)

  def create(self, request, *args, **kwargs):
    request.data.update({ 'user': request.user.id })
    serializer = ImageSerializer(data=request.data)
    print(request.data)

    if serializer.is_valid():
      serializer.save()

      return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

