from django.db import models

class RP(models.Model):
    title = models.CharField(max_length=300)
    url = models.URLField(unique=True)
    published = models.BooleanField(default=False)
    note = models.IntegerField(default=0)

# Create your models here.
