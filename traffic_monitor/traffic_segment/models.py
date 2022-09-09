from django.db import models
from django.utils import timezone

# Create your models here.
class TrafficSegment(models.Model):
    id = models.BigAutoField(primary_key=True, auto_created=True, db_index = True, name="id")
    long_start = models.CharField(name="long_start", max_length=200, default="")
    lat_start = models.CharField(name="lat_start", max_length=200, default="")
    long_end = models.CharField(name="long_end", max_length=200, default="")
    lat_end = models.CharField(name="lat_end", max_length=200, default="")
    length = models.CharField(name="length", max_length=200, default="")
    speed = models.CharField(name="speed", max_length=200, default="")
    timestamp = models.DateTimeField(default=timezone.now)

    def _str_(self):
        return "{ " + self.long_start + ", " + self.lat_start + ", " + self.long_end + ", " + self.lat_end + ", " + self.speed + " }"