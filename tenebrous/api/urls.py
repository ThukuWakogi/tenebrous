from django.urls import include, path
from rest_framework import routers
from . import views
from rest_framework.authtoken.views import ObtainAuthToken
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'images', views.ImageViewSet)

urlpatterns = [
  path('', include(router.urls)),
  path('auth/', views.ObtainAuthTokenAndUserDetails.as_view()),
  path('udft/', views.UserView.as_view())
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
