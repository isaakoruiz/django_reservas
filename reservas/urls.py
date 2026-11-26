from django.urls import path

from . import views

app_name = "reservas"

urlpatterns = [
    path("", views.EspacioListView.as_view(), name="lista"),
    path("espacios/<int:pk>/", views.EspacioDetailView.as_view(), name="detalle"),
]