import logging

logger = logging.getLogger("reservas.peticiones")


class RegistroPeticionesMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            usuario = request.user.username
        else:
            usuario = "anonimo"

        logger.info(
            f"{request.method} {request.path} {response.status_code} {usuario}"
        )

        return response