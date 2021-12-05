from django import template
from ..models import Semence

register = template.Library()


@register.filter()
def get_semence(parcelle, annee):
    semence_id = parcelle[annee]['semence']
    return Semence.objects.get(id=semence_id).name


@register.filter()
def futurist(annee):
    return int(annee) + 20
