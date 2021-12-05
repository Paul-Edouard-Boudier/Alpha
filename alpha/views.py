from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, JsonResponse
from .models import Parcelle, Semence, Annee
import random
from . import evaluation
import pandas as pd
from datetime import datetime
from pathlib import Path


def index(request):
    template = loader.get_template('alpha/index.html')
    parcelles = Parcelle.objects.all()
    semences = Semence.objects.all()
    annees = Annee.objects.all()
    for p in parcelles:
        p.annee_semence = {}
        p.save()

    context = {
        'semences': semences,
        'parcelles': parcelles,
        'annees': annees,
        'my_range': ['1', '2', '3'],
    }

    return HttpResponse(template.render(context, request))


def update_assol(request):
    semences = Semence.objects.all()
    id_parcelle, annee = request.POST.dict()['cellule'].split('-')
    culture = request.POST.dict()['culture']
    parcelle = Parcelle.objects.get(id=id_parcelle)
    note_rotation = None
    update_parcel(parcelle, annee, culture)
    if len(parcelle.annee_semence.keys()) == 3:
        note_rotation = get_note_rotation(parcelle)
    data_user = semences.get(name=culture)
    t_base = 0
    data = pd.read_csv(Path(Path(__file__).parent, 'static', 'weather_data.csv'), sep=',')
    data = data.drop('date_false', axis=1)
    data['date'] = data['date'].apply(lambda x: datetime.strptime(x, '%d/%m/%Y'))
    data['annee'] = data['date'].apply(lambda x: x.year)
    data['t_moy'] = (data['t_min'] + data['t_max']) / 2
    data_user.semis = f"{data_user.semis}/{annee}"
    data_user.semis = datetime.strptime(data_user.semis, '%d/%m/%Y')
    if data_user.annee_recolte == 'n':
        data_user.recolte = f"{data_user.recolte}/{annee}"
    else:
        data_user.recolte = f"{data_user.recolte}/{annee + 1}"
    data_user.recolte = datetime.strptime(data_user.recolte, '%d/%m/%Y')
    somme_cum_pluvio, somme_cum_temp = evaluation.cumulated_sum(data, data_user.semis, data_user.recolte,
                                                                int(data_user.temperature_base))
    note_climat = evaluation.evaluate_climate(somme_cum_pluvio, somme_cum_temp, data_user)
    bilanhydrique = (somme_cum_pluvio >= data_user.besoin_eau)
    besointemperature = (somme_cum_temp >= data_user.besoin_temperature)
    data = {
        'bilanhydrique': bilanhydrique,
        'besointemperature': besointemperature,
        'echaudage': 0,
        'note_climat': note_climat,
        'note_rotation': note_rotation,

        }
    return JsonResponse(data)


def update_parcel(parcelle, annee, culture):
    parcelle.annee_semence[annee] = culture
    parcelle.save()


def get_note_rotation(parcelle):
    data = {}
    for year, culture in parcelle.annee_semence.items():
        data[year] = Semence.objects.get(name=culture)
    return evaluation.evaluate_rotation(data)

# def populate():
# populate()
# s_ids = Semence.objects.all().values_list('id', flat=True)
# for p in Parcelle.objects.all():
#     p.annee_semence = {
#         1: {'semence': random.choice(s_ids)},
#         2: {'semence': random.choice(s_ids)},
#         3: {'semence': random.choice(s_ids)},
#     }
#     p.save()
#     Semence.objects.all().delete()
#     # f = open('./static/populate.json', 'r')
#     # obj = simplejson.load(f)
#
#     populate = [{
#          "name": "Tournesol",
#          "recolte": "01/10",
#          "semis":"01/04",
#          "besoin_eau": 554,
#          "besoin_temperature": 1700 ,
#          "temperature_base": 6,
#          "rang_de_culture": "F" ,
#          "frequence_culture": 6 ,
#          "annee_recolte": "n"
#          },
#          {
#          "name": "Mais doux",
#          "recolte": "01/10",
#          "semis": "01/04",
#          "besoin_eau": 761,
#          "besoin_temperature": 2000,
#         "temperature_base": 10,
#         "rang_de_culture": "C" ,
#         "frequence_culture": 2,
#         "annee_recolte": "n",
#          },
#          {
#          "name": "Soja",
#          "recolte": "15/09",
#          "semis": "15/04",
#          "besoin_eau": 530,
#          "besoin_temperature": 1440,
#         "temperature_base": 6,
#         "rang_de_culture": "T" ,
#         "frequence_culture": 3,
#         "annee_recolte": "n"
#          },
#          {
#          "name": "Blé tendre",
#          "semis": "01/10",
#          "recolte": "01/06",
#          "besoin_eau": 660,
#          "besoin_temperature": 1600,
#         "temperature_base": 0,
#         "rang_de_culture": "C",
#         "frequence_culture": 3,
#         "annee_recolte": "n+1"
#          },
#          {
#          "name": "Blé dur",
#          "semis": "01/02",
#          "recolte": "01/09",
#          "besoin_eau": 430,
#          "besoin_temperature": 2400,
#         "temperature_base": 0,
#         "rang_de_culture": "C" ,
#         "frequence_culture": 3,
#         "annee_recolte": "n"
#          },
#          {
#          "name": "Luzerne",
#          "semis": "15/04",
#          "recolte": "15/10",
#          "besoin_eau": 1342,
#          "besoin_temperature": 400,
#         "temperature_base": 5,
#         "rang_de_culture": "T",
#         "frequence_culture": 0,
#         "annee_recolte": "n"
#          },
#          {
#              "name": "Jachère",
#              "semis": "",
#              "recolte": "",
#              "besoin_eau": 0,
#              "besoin_temperature": 0,
#              "temperature_base": 0,
#              "rang_de_culture": "",
#              "frequence_culture": 0,
#              "annee_recolte": ""
#              }
#     ]
#     for record in populate:
#         # import ipdb; ipdb.set_trace()
#         Semence.objects.create(
#             name=record["name"],
#             recolte=record["recolte"],
#             semis=record["semis"],
#             besoin_eau=record["besoin_eau"],
#             besoin_temperature=record["besoin_temperature"],
#             temperature_base=record["temperature_base"],
#             rang_de_culture=record["rang_de_culture"],
#             frequence_culture=record["frequence_culture"],
#             annee_recolte=record["annee_recolte"],
#         )
        # for key in record.keys():
        #     s.__setattr__(key, record[key])
        # s.save()


        # record = Country(name = o)
        # record.save()


    # for s in test:
    #     Semence.objects.create(
    #         name=s['name'],
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
