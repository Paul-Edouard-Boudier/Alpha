from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import Parcelle, Semence, Annee
import random

# Create your views here.


def index(request):
    template = loader.get_template('alpha/index.html')
    parcelles = Parcelle.objects.all()
    semences = Semence.objects.all()
    annees = Annee.objects.all()
    # s_ids = Semence.objects.all().values_list('id', flat=True)
    # for p in Parcelle.objects.all():
    #     p.annee_semence = {
    #         1: {'semence': random.choice(s_ids)},
    #         2: {'semence': random.choice(s_ids)},
    #         3: {'semence': random.choice(s_ids)},
    #     }
    #     p.save()
    context = {
        'semences': semences,
        'parcelles': parcelles,
        'annees': annees,
        'my_range': ['1', '2', '3']
    }
    return HttpResponse(template.render(context, request))


# def populate(request):
    # test = [
    #     {
    #         "nom": "Tournesol",
    #         # date ? date en string ?
    #         "recolte": "01/10/2020",
    #         "semis": "01/04/2020",
    #         # besoin en mm (par m2 d'exploitation ?)
    #         "besoin_eau": 554,
    #         "besoin_temperature": 1700,
    #     },
    #     {
    #         "nom": "Mais doux",
    #         # date ? date en string ?
    #         "recolte": "01/10/2020",
    #         "semis": "01/04/2020",
    #         # besoin en mm (par m2 d'exploitation ?)
    #         "besoin_eau": 761,
    #         "besoin_temperature": 2000,
    #     },
    #     {
    #         "nom": "Soja",
    #         # date ? date en string ?
    #         "recolte": "15/09/2020",
    #         "semis": "15/04/2020",
    #         # besoin en mm (par m2 d'exploitation ?)
    #         "besoin_eau": 530,
    #         "besoin_temperature": 1440,
    #     },
    #     {
    #         "nom": "Blé tendre",
    #         # date ? date en string ?
    #         "recolte": "01/10/2020",
    #         "semis": "01/06/2020",
    #         # besoin en mm (par m2 d'exploitation ?)
    #         "besoin_eau": 660,
    #         "besoin_temperature": 1600,
    #     },
    #     {
    #         "nom": "Blé dur",
    #         "recolte": "01/02/2020",
    #         "semis": "01/09/2020",
    #         "besoin_eau": 430,
    #         "besoin_temperature": 2400,
    #     },
    #     {
    #         "nom": "Luzerne",
    #         "recolte": "15/04/2020",
    #         "semis": "15/10/2020",
    #         "besoin_eau": 1342,
    #         "besoin_temperature": 400,
    #     }
    # ]
    # for s in test:
    #     Semence.objects.create(
    #         name=s['nom'],
    #         semis=s['semis'],
    #         recolte=s['recolte'],
    #         besoin_eau=s['besoin_eau'],
    #         besoin_temperature=s['besoin_temperature']
    #     )
    # for i in range(3):
    #     Annee.objects.create(
    #         name=i,
    #         parcelles
    #     )
