from django.contrib.auth.models import *
from django.db import *
import uuid

from django.db import models

# Model untuk Itinerary
class Itinerary(models.Model):
    name = models.CharField(max_length=255)
    cover = models.ImageField(upload_to='trip_covers/', blank=True, null=True)

    def __str__(self):
        return self.name

# Model untuk Hari dalam Itinerary
class Day(models.Model):
    itinerary = models.ForeignKey(Itinerary, related_name='days', on_delete=models.CASCADE)
    day_number = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return f"Day {self.day_number} - {self.date}"

# Model untuk Destinasi dalam Hari
class Destination(models.Model):
    day = models.ForeignKey(Day, related_name='destinations', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    time = models.TimeField()

    def __str__(self):
        return f"{self.name} at {self.time}"
