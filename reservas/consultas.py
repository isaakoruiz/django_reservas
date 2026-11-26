
from django.db.models import Count, Q

from .models import Espacio


def ocupacion(fecha):
    return Espacio.objects.filter(activo=True).annotate(
        reservas_confirmadas=Count(
            "reservas",
            filter=Q(
                reservas__fecha=fecha,
                reservas__estado="confirmada"
            )
        )
    ).order_by("-reservas_confirmadas", "nombre")
