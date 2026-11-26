from django.contrib.auth.models import Permission
from datetime import date, time

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reservas.models import Espacio, Reserva


class Command(BaseCommand):

    def handle(self, *args, **options):
        Usuario = get_user_model()

        Reserva.objects.all().delete()

        usuarios = {}

        datos_usuarios = [
            ("profe1", False),
            ("profe2", False),
            ("conserje", True),
        ]

        for nombre, es_personal in datos_usuarios:
            usuario, creado = Usuario.objects.get_or_create(
                username=nombre,
                defaults={"is_staff": es_personal}
            )

            usuario.is_staff = es_personal
            usuario.set_password("Clave.2026")
            usuario.save()

            usuarios[nombre] = usuario
            if nombre == "conserje":
                permisos = Permission.objects.filter(
                    content_type__app_label="reservas",
                    content_type__model__in=["espacio", "reserva"]
                )
                usuario.user_permissions.set(permisos)

        datos_espacios = [
            ("Aula 12", "aula", 30, True),
            ("Laboratorio de Física", "laboratorio", 24, True),
            ("Salón de actos", "salon", 200, True),
            ("Pista polideportiva", "pista", 60, True),
            ("Aula 3", "aula", 25, False),
        ]

        espacios = {}

        for nombre, tipo, aforo, activo in datos_espacios:
            espacio, creado = Espacio.objects.update_or_create(
                nombre=nombre,
                defaults={
                    "tipo": tipo,
                    "aforo": aforo,
                    "activo": activo
                }
            )

            espacios[nombre] = espacio

        datos_reservas = [
            ("Aula 12", date(2027, 5, 20), time(9, 0), time(10, 0),
             "profe1", "confirmada", "Examen de Matemáticas"),

            ("Aula 12", date(2027, 5, 20), time(10, 0), time(11, 0),
             "profe2", "confirmada", "Tutoría de 2.ºDAW"),

            ("Salón de actos", date(2027, 5, 20), time(12, 0), time(14, 0),
             "profe1", "pendiente", "Charla de orientación"),

            ("Laboratorio de Física", date(2027, 5, 24), time(8, 30), time(10, 20),
             "profe2", "confirmada", "Práctica de óptica"),

            ("Pista polideportiva", date(2027, 5, 24), time(11, 15), time(12, 10),
             "profe1", "cancelada", "Torneo de recreo"),

            ("Aula 12", date(2027, 5, 24), time(9, 0), time(10, 0),
             "profe1", "pendiente", "Recuperación"),
        ]

        for nombre, fecha, inicio, fin, usuario, estado, motivo in datos_reservas:
            Reserva.objects.create(
                espacio=espacios[nombre],
                fecha=fecha,
                hora_inicio=inicio,
                hora_fin=fin,
                usuario=usuarios[usuario],
                estado=estado,
                motivo=motivo
            )

        self.stdout.write(
            self.style.SUCCESS("Cargados 5 espacios y 6 reservas.")
        )
