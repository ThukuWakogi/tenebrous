from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
  image = models.ImageField(upload_to='images/')
  bio = models.TextField()
  user = models.ForeignKey(User, on_delete=models.CASCADE)

class Image(models.Model):
  image = models.ImageField(upload_to='images/')
  name = models.CharField(max_length=500)
  caption = models.CharField(max_length=500)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

class ImageLikes(models.Model):
  image = models.ForeignKey(Image, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

class ImageComments(models.Model):
  image = models.ForeignKey(Image, on_delete=models.CASCADE)
  image_comment = models.CharField(max_length=500)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
