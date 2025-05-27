from django.db import models

# Create your models here.
class Overmij(models.Model):
    subtitel = models.CharField(max_length=200)
    tekst = models.TextField()
    afbeelding = models.ImageField(upload_to='overmij_afbeelding/', null=True, blank=True)


class Footer(models.Model):
    tekst = models.TextField()
    email = models.EmailField(null=True, blank=True)
