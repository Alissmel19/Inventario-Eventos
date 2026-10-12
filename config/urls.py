from django.contrib import admin
from django.urls import path, include
from eventos import views



urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "",
        include("eventos.urls")
    ),

    path(
    "hospedaje/disponibilidad/",
    views.habitaciones_disponibles,
    name="habitaciones_disponibles"
),


path(
    "hospedaje/cotizar/",
    views.cotizar_hospedaje,
    name="cotizar_hospedaje"
),
]
