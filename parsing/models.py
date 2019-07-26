from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.


class Hotel(models.Model):
    id_lt = models.IntegerField(unique=True)
    name = models.CharField(max_length=250)
    stars = models.PositiveIntegerField()
    country = models.CharField(max_length=30)
    num_empty_rooms = models.IntegerField()
    href = models.URLField()

    def __str__(self):
        return self.name


