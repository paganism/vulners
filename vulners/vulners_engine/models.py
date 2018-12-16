from django.db import models
from datetime import datetime


class Vulner(models.Model):
    vendor = models.CharField(max_length=100)
    vulner = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=5000)
    published = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.vulner

    class Meta:
        ordering = ['-published']
