from django.urls import path
from . import views


urlpatterns = [

    # Dashboard
    path(
        "",
        views.dashboard,
        name="dashboard"
    ),

    # Nueva cotización
    path(
        "cotizaciones/nueva/",
        views.nueva_cotizacion,
        name="nueva_cotizacion"
    ),

    # Registro de eventos
    path(
        "eventos/",
        views.registro_eventos,
        name="registro_eventos"
    ),

    # Cerrar sesión
    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),
]