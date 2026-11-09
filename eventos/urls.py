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
    
    path(
        "cotizaciones/<int:cotizacion_id>/pdf/",
        views.pdf_cotizacion,
        name="pdf_cotizacion",
    ),

    path(
    "reservas-web/",
    views.reservas_web,
    name="reservas_web"
    ),

    path(
        "reservas-web/<int:reserva_id>/",
        views.detalle_reserva_web,
        name="detalle_reserva_web"
    ),

    path(
        "reservas-web/<int:reserva_id>/rechazar/",
        views.rechazar_reserva_web,
        name="rechazar_reserva_web"
    ),

]