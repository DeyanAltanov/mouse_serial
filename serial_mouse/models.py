from django.db import models


class Capture(models.Model):
    image = models.ImageField(upload_to='captures/')
    timestamp = models.DateTimeField(auto_now_add=True)


class MouseData(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)