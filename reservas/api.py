from datetime import date

from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import EsPersonalOSoloLectura, EsPropietarioOSoloLectura

from .models import Espacio, Reserva
from .serializers import EspacioSerializer, ReservaSerializer
from .consultas import ocupacion


class EspacioViewSet(viewsets.ModelViewSet):
    queryset = Espacio.objects.all()
    serializer_class = EspacioSerializer
    permission_classes = [EsPersonalOSoloLectura]

    def get_queryset(self):
        queryset = super().get_queryset()

        tipo = self.request.query_params.get("tipo")
        activo = self.request.query_params.get("activo")

        if tipo:
            queryset = queryset.filter(tipo=tipo)

        if activo is not None:
            if activo.lower() == "true":
                queryset = queryset.filter(activo=True)
            elif activo.lower() == "false":
                queryset = queryset.filter(activo=False)

        return queryset

    def destroy(self, request, *args, **kwargs):
        espacio = self.get_object()

        if espacio.reservas.exists():
            return Response(
                {"detail": "El espacio tiene reservas y no se puede borrar."},
                status=status.HTTP_409_CONFLICT
            )

        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=["get"], url_path="ocupacion")
    def ocupacion_del_dia(self, request):
        fecha_texto = request.query_params.get("fecha")

        if not fecha_texto:
            return Response(
                {"detail": "Falta el parámetro fecha (AAAA-MM-DD)."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            fecha = date.fromisoformat(fecha_texto)
        except ValueError:
            raise serializers.ValidationError({
                "fecha": "Formato de fecha no válido (AAAA-MM-DD)."
            })

        espacios = ocupacion(fecha)

        resultado = [
            {
                "id": espacio.id,
                "nombre": espacio.nombre,
                "reservas_confirmadas": espacio.reservas_confirmadas
            }
            for espacio in espacios
        ]

        return Response(resultado)


class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.select_related("espacio", "usuario")
    serializer_class = ReservaSerializer
    permission_classes = [IsAuthenticated, EsPropietarioOSoloLectura]
    
    def get_queryset(self):
        queryset = super().get_queryset()

        fecha_texto = self.request.query_params.get("fecha")
        espacio = self.request.query_params.get("espacio")
        estado = self.request.query_params.get("estado")

        if fecha_texto:
            try:
                fecha = date.fromisoformat(fecha_texto)
            except ValueError:
                raise serializers.ValidationError({
                    "fecha": "Formato de fecha no válido (AAAA-MM-DD)."
                })

            queryset = queryset.filter(fecha=fecha)

        if espacio:
            if not espacio.isdigit():
                raise serializers.ValidationError({
                    "espacio": "Debe ser un número."
                })

            queryset = queryset.filter(espacio_id=int(espacio))

        if estado:
            queryset = queryset.filter(estado=estado)

        return queryset

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)