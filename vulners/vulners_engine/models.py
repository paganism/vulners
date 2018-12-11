from django.db import models

# Create your models here.

class Vulner(models.Model):
    vendor = models.CharField(max_length=100)
    vulner = models.CharField(max_length=100)
    description = models.TextField(max_length=5000)
    published = models.CharField(max_length=50)

    def __str__(self):
        return self.vulner