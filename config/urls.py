from django.contrib import admin
from django.urls import path, include
from eventos import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),


    path("login/", views.login_view, name="login"),




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


    path(
        "hospedaje/guardar/",
        views.guardar_cotizacion_hospedaje,
        name="guardar_cotizacion_hospedaje",
    ),

    path(
        "pagos/registrar/",
        views.registrar_pago,
        name="registrar_pago",
    ),


    path(
        "pagos/nuevo/",
        views.formulario_pago,
        name="formulario_pago",
    ),
    
    path(
        "cotizaciones/",
        views.lista_cotizaciones,
        name="lista_cotizaciones",
    ),
    path(
        "cotizaciones/<int:cotizacion_id>/estado/",
        views.actualizar_estado_cotizacion,
        name="actualizar_estado_cotizacion",
    ),
    path(
    "cotizaciones/<int:cotizacion_id>/detalle/",
    views.detalle_cotizacion,
    name="detalle_cotizacion",
    ),


        
    path(
        "pagos/cotizacion/<int:cotizacion_id>/",
        views.pagos_cotizacion_json,
        name="pagos_cotizacion_json",
    ),
    
    path(
        "pagos/<int:pago_id>/validar/",
        views.validar_pago,
        name="validar_pago",
    ),




]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )