from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import Espacio, Reserva


class EspacioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Espacio
        fields = ["id", "nombre", "tipo", "aforo", "activo"]


class ReservaSerializer(serializers.ModelSerializer):
    espacio_nombre = serializers.CharField(
        source="espacio.nombre",
        read_only=True
    )
    usuario = serializers.CharField(
        source="usuario.username",
        read_only=True
    )

    class Meta:
        model = Reserva
        fields = [
            "id",
            "espacio",
            "espacio_nombre",
            "usuario",
            "fecha",
            "hora_inicio",
            "hora_fin",
            "motivo",
            "estado",
            "creada"
        ]
        read_only_fields = ["estado", "creada"]

    def validate(self, attrs):
        if self.instance:
            reserva = Reserva(
                pk=self.instance.pk,
                espacio=attrs.get("espacio", self.instance.espacio),
                usuario=self.instance.usuario,
                fecha=attrs.get("fecha", self.instance.fecha),
                hora_inicio=attrs.get("hora_inicio", self.instance.hora_inicio),
                hora_fin=attrs.get("hora_fin", self.instance.hora_fin),
                motivo=attrs.get("motivo", self.instance.motivo),
                estado=self.instance.estado,
                creada=self.instance.creada
            )
        else:
            reserva = Reserva(**attrs)

        try:
            reserva.clean()
        except ValidationError as error:
            raise serializers.ValidationError(
                error.message_dict if hasattr(error, "error_dict") else error.messages
            )

        return attrs