from django.db import models
import uuid

# Create your models here.

class Place(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title


class PlaceCollection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    places = models.ManyToManyField(Place)
    progress = models.IntegerField(default=0)

    def __str__(self):
        return self.name
