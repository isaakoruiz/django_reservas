from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Espacio, Reserva
from .forms import ReservaForm


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


class ReservaCreateView(LoginRequiredMixin, CreateView):
    form_class = ReservaForm
    template_name = "reservas/reserva_form.html"
    success_url = reverse_lazy("reservas:mias")

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class MisReservasView(LoginRequiredMixin, ListView):
    template_name = "reservas/mis_reservas.html"
    context_object_name = "reservas"

    def get_queryset(self):
        return Reserva.objects.filter(
            usuario=self.request.user
        ).select_related("espacio")