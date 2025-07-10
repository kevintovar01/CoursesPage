# Django
from django.db.models import F, Value
from django.db.models.functions import Concat
from .models import User


def get_registered_users_detailed():
    return (
        User.objects
        .annotate(
            full_name=Concat(F('first_name'), Value(' '), F('last_name'))
        ).select_related('country')
        .select_related('roles')
        .values(
            'id', 'full_name', 
            correoUsuario=F('email'),
            nombrePais=F('country__name'),
            nombreRole=F('roles__name')
        ).order_by('id')
    )