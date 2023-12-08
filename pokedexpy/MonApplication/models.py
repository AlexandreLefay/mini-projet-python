from django.db import models

# Create your models here.
class Pokemon(models.Model):
    nom = models.CharField(max_length=100)
    pokemon_id = models.IntegerField(unique=True)
    types = models.CharField(max_length=100)
    sprite = models.URLField()

    def __str__(self):
        return self.nom
