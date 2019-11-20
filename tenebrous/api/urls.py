from django.urls import include, path
from rest_framework import routers
from . import views
from rest_framework.authtoken.views import ObtainAuthToken

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
  path('', include(router.urls)),
  path('auth/', views.ObtainAuthTokenAndUserDetails.as_view()),
  path('udft/', views.UserView.as_view())
]
