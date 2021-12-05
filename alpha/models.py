from django.db import models

# Create your models here.


class Semence(models.Model):
    """
    fiche de culture classique utilisée dans le tableau
    """
    name = models.CharField(max_length=30, null=True)
    semis = models.CharField(max_length=100, null=True)
    recolte = models.CharField(max_length=100, null=True)
    besoin_eau = models.IntegerField(null=True)
    besoin_temperature = models.IntegerField(null=True)
    temperature_base = models.CharField(max_length=30, null=True, default="")
    rang_de_culture = models.CharField(max_length=1, null=True, default="")
    frequence_culture = models.IntegerField(null=True, default=1)
    annee_recolte = models.CharField(max_length=3, null=True, default="")


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
