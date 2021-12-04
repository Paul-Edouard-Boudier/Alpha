from django.db import models

# Create your models here.


class Semence(models.Model):
    """
    fiche de culture classique utilisée dans le tableau
    """
    name = models.CharField(max_length=30)
    semis = models.CharField(max_length=100)
    recolte = models.CharField(max_length=100)
    besoin_eau = models.IntegerField()
    besoin_temperature = models.IntegerField()


class Annee(models.Model):
    """L'année à partir de laquelle on va calculer le score.
    Contient des parcelles.
    """
    name = models.CharField(max_length=30)


class Parcelle(models.Model):
    """
    """
    name = models.CharField(max_length=30)
    # title="taille de la parcelle"
    taille = models.IntegerField()
    annee_semence = models.JSONField()
    # semence = models.ForeignKey(Semence, on_delete=models.CASCADE, null=True)
    # annees = models.ManyToManyField(Annee)
