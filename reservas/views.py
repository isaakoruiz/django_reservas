
from django.utils import timezone
from django.views.generic import DetailView, ListView

from .models import Espacio, Reserva


class EspacioListView(ListView):
    template_name = "reservas/lista.html"
    context_object_name = "espacios"

    def get_queryset(self):
        return Espacio.objects.filter(activo=True)


class EspacioDetailView(DetailView):
    model = Espacio
    template_name = "reservas/detalle.html"
    context_object_name = "espacio"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)

        contexto["reservas"] = self.object.reservas.filter(
            estado=Reserva.Estado.CONFIRMADA,
            fecha__gte=timezone.localdate()
        ).select_related("usuario")

        return contexto
