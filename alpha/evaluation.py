import pandas as pd
from datetime import datetime


def select_data(data, date_semis, date_recolte, t_base):
    data_annee = data[data['date'] >= date_semis]
    data_annee = data_annee[data_annee['date'] <= date_recolte]
    data_annee['degre_jour'] = data_annee['t_moy'].apply(lambda x: max(x - t_base, 0))
    data_annee['date_jour_mois'] = data_annee['date'].apply(lambda x: x.strftime('%d/%m'))

    return data_annee


def cumulated_sum(data, date_semis, date_recolte, t_base):
    date_semis_n_moins_1 = datetime(date_semis.year - 1, date_semis.month, date_semis.day)
    date_semis_n_plus_1 = datetime(date_semis.year + 1, date_semis.month, date_semis.day)
    date_recolte_n_moins_1 = datetime(date_recolte.year - 1, date_recolte.month, date_recolte.day)
    date_recolte_n_plus_1 = datetime(date_recolte.year + 1, date_recolte.month, date_recolte.day)

    data_annee_n_moins_1 = select_data(data, date_semis_n_moins_1, date_recolte_n_moins_1, t_base)
    data_annee_n = select_data(data, date_semis, date_recolte, t_base)
    data_annee_n_plus_1 = select_data(data, date_semis_n_plus_1, date_recolte_n_plus_1, t_base)

    data_final = data_annee_n.merge(data_annee_n_moins_1[['date_jour_mois', 't_moy', 'pluvio', 'degre_jour']],
                                    on='date_jour_mois')
    data_final = data_final.merge(data_annee_n_plus_1[['date_jour_mois', 't_moy', 'pluvio', 'degre_jour']],
                                  on='date_jour_mois')
    data_final['pluvio_moy'] = data_final[['pluvio', 'pluvio_x', 'pluvio_y']].mean(axis=1)
    data_final['degre_jour_moy'] = data_final[['degre_jour', 'degre_jour_x', 'degre_jour_y']].mean(axis=1)

    somme_cum_pluvio = round(float(data_final['pluvio'].cumsum()[-1:]), 0)
    somme_cum_temp = round(float(data_final['degre_jour'].cumsum()[-1:]), 0)
    return somme_cum_pluvio, somme_cum_temp


def evaluate_climate(somme_cum_pluvio, somme_cum_temp, fiche_culture):
    note_climat = 0
    if somme_cum_pluvio >= fiche_culture.besoin_eau:
        note_climat += 1
    if somme_cum_temp >= fiche_culture.besoin_temperature:
        note_climat += 1
    return note_climat


def evaluate_rotation(cultures_parcelle):
    note_rotation = 0
    for annee_index in range(1, len(cultures_parcelle.keys())):
        annee_n_moins_1 = list(cultures_parcelle.keys())[annee_index - 1]
        annee_n = list(cultures_parcelle.keys())[annee_index]
        rang_n_moins_1 = cultures_parcelle[str(annee_n_moins_1)].rang_de_culture
        rang_n = cultures_parcelle[str(annee_n)].rang_de_culture
        if (rang_n_moins_1 == 'T' and rang_n == 'C') or (rang_n_moins_1 == 'C' and rang_n == 'F') or (rang_n_moins_1 == 'F' and rang_n == 'T'):
            note_rotation += 1
    return note_rotation
