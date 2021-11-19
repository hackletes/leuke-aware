from django.db import models

# Create your models here.

class Badge(models.Model):
    name = models.CharField(max_length=64, null = True)
    image = models.ImageField(upload_to = 'tasks')