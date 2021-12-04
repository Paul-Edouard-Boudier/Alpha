from django import template
from ..models import Semence

register = template.Library()


@register.filter()
def get_semence(parcelle, annee):
    # import ipdb; ipdb.set_trace()
    semence_id = parcelle[annee]['semence']
    return Semence.objects.get(id=semence_id).name
