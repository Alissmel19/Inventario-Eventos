from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import (
    Clientes,
    Eventos,
    Cotizaciones,
    Pagos,
)


# ============================================================
# LOGIN
# ============================================================

def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        return render(
            request,
            "login.html",
            {
                "error": "Usuario o contraseña incorrectos."
            }
        )

    return render(request, "login.html")


# ============================================================
# DASHBOARD GENERAL
# ============================================================

@login_required(login_url="login")
def dashboard(request):

    context = {
        "total_clientes": Clientes.objects.count(),
        "total_eventos": Eventos.objects.count(),
        "total_cotizaciones": Cotizaciones.objects.count(),
        "total_pagos": Pagos.objects.count(),
    }

    return render(
        request,
        "dashboard.html",
        context
    )


# ============================================================
# CERRAR SESIÓN
# ============================================================

def logout_view(request):

    logout(request)

    return redirect("login")


# ============================================================
# DATOS TEMPORALES DE EVENTOS
# ============================================================

def obtener_eventos_temporales():

    return [

        {
            "numero": "COT-001",
            "cliente": "María López",
            "evento": "Boda",
            "tipo": "Boda",
            "fecha": "15/10/2026",
            "hora": "4:00 PM - 9:00 PM",
            "personas": 50,
            "lugar": "Salón VIP",
            "estado": "Pendiente",
            "total": 2131.25,
            "paquete": "Paquete VIP",
            "telefono": "7123-4567",
            "correo": "maria@email.com",
            "observaciones": "Ceremonia en jardín.",
        },

        {
            "numero": "COT-002",
            "cliente": "Empresa ABC",
            "evento": "Cena corporativa",
            "tipo": "Corporativo",
            "fecha": "20/10/2026",
            "hora": "6:00 PM - 10:00 PM",
            "personas": 80,
            "lugar": "Terraza Principal",
            "estado": "Confirmado",
            "total": 3450.00,
            "paquete": "Evento por Consumo",
            "telefono": "2234-5678",
            "correo": "eventos@empresaabc.com",
            "observaciones": "Montaje corporativo.",
        },

        {
            "numero": "COT-003",
            "cliente": "Carlos Martínez",
            "evento": "Cumpleaños",
            "tipo": "Social",
            "fecha": "25/10/2026",
            "hora": "5:00 PM - 9:00 PM",
            "personas": 40,
            "lugar": "Restaurante",
            "estado": "Finalizado",
            "total": 1280.00,
            "paquete": "Evento por Consumo",
            "telefono": "7012-3456",
            "correo": "carlos@email.com",
            "observaciones": "Celebración familiar.",
        },

        {
            "numero": "COT-004",
            "cliente": "Ana Rodríguez",
            "evento": "Graduación",
            "tipo": "Graduación",
            "fecha": "02/11/2026",
            "hora": "3:00 PM - 8:00 PM",
            "personas": 65,
            "lugar": "Salón Las Orquídeas",
            "estado": "Pendiente",
            "total": 2750.00,
            "paquete": "Evento por Consumo + Salón Las Orquídeas",
            "telefono": "7456-7890",
            "correo": "ana@email.com",
            "observaciones": "Se requiere proyector.",
        },

        {
            "numero": "COT-005",
            "cliente": "Corporación XYZ",
            "evento": "Conferencia empresarial",
            "tipo": "Corporativo",
            "fecha": "08/11/2026",
            "hora": "8:00 AM - 2:00 PM",
            "personas": 120,
            "lugar": "Terraza Secundaria",
            "estado": "Confirmado",
            "total": 4200.00,
            "paquete": "Evento por Consumo + Salón Las Orquídeas",
            "telefono": "2222-3333",
            "correo": "eventos@xyz.com",
            "observaciones": "Evento empresarial.",
        },

        {
            "numero": "COT-006",
            "cliente": "Sofía Hernández",
            "evento": "Baby Shower",
            "tipo": "Social",
            "fecha": "14/11/2026",
            "hora": "2:00 PM - 6:00 PM",
            "personas": 35,
            "lugar": "Restaurante",
            "estado": "Cancelado",
            "total": 950.00,
            "paquete": "Evento por Consumo",
            "telefono": "7234-5678",
            "correo": "sofia@email.com",
            "observaciones": "Evento cancelado por el cliente.",
        },

    ]


# ============================================================
# PAQUETES TEMPORALES
# ============================================================

def obtener_paquetes():

    return [

        {
            "id": "consumo",
            "nombre": "Evento por Consumo",
            "subtitulo": "Paquete 1",
            "descripcion": (
                "Ideal para celebraciones dentro del restaurante."
            ),
            "precio": "Consumo",
            "tipo_precio": "consumo",
            "incluye": [
                "Elección de entrada",
                "Elección de plato fuerte",
                "Elección de bebida",
                "Elección de postre",
                "Reserva de espacio dentro del restaurante",
            ],
            "nota": (
                "No permite bocinas, música, baile ni DJ. "
                "Se agrega 10% de propina sobre el consumo."
            ),
        },

        {
            "id": "orquideas",
            "nombre": "Evento por Consumo + Salón Las Orquídeas",
            "subtitulo": "Paquete 2",
            "descripcion": (
                "Evento privado en un espacio equipado."
            ),
            "precio": 250.00,
            "tipo_precio": "fijo",
            "incluye": [
                "Elección de entrada",
                "Elección de plato fuerte",
                "Elección de bebida",
                "Elección de postre",
                "5 horas de Salón Las Orquídeas",
                "Aire acondicionado",
                "Sonido profesional",
                "Uso de proyector",
                "Mesas y sillas",
            ],
            "nota": (
                "$250 por 5 horas más el consumo de alimentos "
                "y bebidas. Se agrega 10% de propina."
            ),
        },

        {
            "id": "vip",
            "nombre": "Paquete VIP",
            "subtitulo": "Experiencia completa",
            "descripcion": (
                "Alimentación, bebidas, montaje y servicio "
                "para los invitados."
            ),
            "precio": "Desde $33.75 p/p",
            "tipo_precio": "persona",
            "incluye": [
                "Ensalada Caprese con pesto de la casa",
                "Elección de plato fuerte",
                "Refil de gaseosa",
                "Estación de café",
                "Base de plato + copa",
                "Manteles",
                "Servilletas de tela",
                "Florero",
                "Descorche de pastel",
                "Meseros exclusivos",
                "Uso de jardín para ceremonia",
            ],
            "nota": (
                "Vegetariano $33.75 p/p · Pollo $37.25 p/p · "
                "Carne $40.75 p/p. Se agrega 10% de propina."
            ),
        },

    ]


# ============================================================
# HOME DE EVENTOS
# ============================================================

@login_required(login_url="login")
def eventos_home(request):

    eventos = obtener_eventos_temporales()
    paquetes = obtener_paquetes()

    context = {
        "eventos": eventos,
        "paquetes": paquetes,

        "total_eventos": len(eventos),

        "pendientes": sum(
            1
            for evento in eventos
            if evento["estado"] == "Pendiente"
        ),

        "confirmados": sum(
            1
            for evento in eventos
            if evento["estado"] == "Confirmado"
        ),

        "finalizados": sum(
            1
            for evento in eventos
            if evento["estado"] == "Finalizado"
        ),

        "cancelados": sum(
            1
            for evento in eventos
            if evento["estado"] == "Cancelado"
        ),
    }

    return render(
        request,
        "EventosHome.html",
        context
    )


# ============================================================
# DETALLE DEL EVENTO
# ============================================================

@login_required(login_url="login")
def detalle_evento(request, numero):

    eventos = obtener_eventos_temporales()

    evento = next(
        (
            evento
            for evento in eventos
            if evento["numero"] == numero
        ),
        None
    )

    if evento is None:
        return redirect("eventos_home")

    return render(
        request,
        "EventosHome.html",
        {
            "evento": evento
        }
    )


# ============================================================
# NUEVA COTIZACIÓN
# ============================================================

@login_required(login_url="login")
def nueva_cotizacion(request):

    # ========================================================
    # LUGARES
    # ========================================================

    lugares = [
        "Terraza Principal",
        "Terraza Secundaria",
        "Salón Las Orquídeas",
        "Restaurante",
        "Salón VIP",
        "Otro",
    ]

    # ========================================================
    # TIPOS DE EVENTO
    # ========================================================

    tipos_evento = [
        "Boda",
        "Graduación",
        "Cumpleaños",
        "Evento corporativo",
        "Conferencia",
        "Reunión empresarial",
        "Baby Shower",
        "XV años",
        "Cena",
        "Aniversario",
        "Otro",
    ]

    # ========================================================
    # CATÁLOGO TEMPORAL
    # ========================================================

    catalogo = [

        {
            "nombre": "Entrada de ensalada caprese con pesto de la casa",
            "tipo": "Servicio de alimentos",
            "precio": 3.50,
            "unidad": "persona",
        },

        {
            "nombre": "Plato de pollo",
            "tipo": "Servicio de alimentos",
            "precio": 21.50,
            "unidad": "persona",
        },

        {
            "nombre": "Refil de gaseosa",
            "tipo": "Bebidas",
            "precio": 2.50,
            "unidad": "persona",
        },

        {
            "nombre": "Estación de café",
            "tipo": "Bebidas",
            "precio": 1.50,
            "unidad": "persona",
        },

        {
            "nombre": "Base de plato",
            "tipo": "Montaje",
            "precio": 1.50,
            "unidad": "persona",
        },

        {
            "nombre": "Copa",
            "tipo": "Montaje",
            "precio": 1.50,
            "unidad": "persona",
        },

        {
            "nombre": "Servilleta de tela",
            "tipo": "Montaje",
            "precio": 0.50,
            "unidad": "persona",
        },

        {
            "nombre": "Meseros",
            "tipo": "Personal",
            "precio": 2.00,
            "unidad": "persona",
        },

        {
            "nombre": "Florero",
            "tipo": "Decoración",
            "precio": 0.25,
            "unidad": "persona",
        },

        {
            "nombre": "Descorche de pastel",
            "tipo": "Servicio",
            "precio": 1.00,
            "unidad": "persona",
        },

        {
            "nombre": "Servicio de sonido y luces",
            "tipo": "Servicios",
            "precio": 125.00,
            "unidad": "evento",
        },

        {
            "nombre": "Manteles",
            "tipo": "Montaje",
            "precio": 0.50,
            "unidad": "persona",
        },

    ]

    # ========================================================
    # SERVICIOS VARIABLES
    # ========================================================

    variables = [

        {
            "nombre": "Descorche de boquitas",
            "descripcion": "$25 por cada opción de boquita seleccionada.",
            "precio": 25.00,
            "unidad": "opción",
        },

        {
            "nombre": "2 horas de barra libre",
            "descripcion": "Servicio de barra libre después de la cena.",
            "precio": 10.00,
            "unidad": "persona",
        },

        {
            "nombre": "Hora extra",
            "descripcion": "Hora adicional de evento.",
            "precio": 150.00,
            "unidad": "hora",
        },

        {
            "nombre": "DJ",
            "descripcion": "Servicio de DJ por 5 horas.",
            "precio": 150.00,
            "unidad": "evento",
        },

    ]

    # ========================================================
    # CATEGORÍAS ÚNICAS
    # ========================================================

    categorias = list(
        dict.fromkeys(
            item["tipo"]
            for item in catalogo
        )
    )

    # ========================================================
    # PAQUETES
    # ========================================================

    paquetes = obtener_paquetes()

    # ========================================================
    # CONTEXTO
    # ========================================================

    context = {
        "lugares": lugares,
        "tipos_evento": tipos_evento,
        "catalogo": catalogo,
        "variables": variables,
        "categorias": categorias,
        "paquetes": paquetes,
    }

    return render(
        request,
        "cotizacionNueva.html",
        context
    )



@login_required(login_url="login")
def registro_eventos(request):

    eventos = [
        {
            "numero": "COT-001",
            "cliente": "María López",
            "evento": "Boda",
            "tipo": "Boda",
            "fecha": "15/10/2026",
            "hora": "4:00 PM - 9:00 PM",
            "personas": 50,
            "lugar": "Salón VIP",
            "estado": "Pendiente",
            "total": 2131.25,
        },
        {
            "numero": "COT-002",
            "cliente": "Empresa ABC",
            "evento": "Cena corporativa",
            "tipo": "Corporativo",
            "fecha": "20/10/2026",
            "hora": "6:00 PM - 10:00 PM",
            "personas": 80,
            "lugar": "Terraza Principal",
            "estado": "Confirmado",
            "total": 3450.00,
        },
        {
            "numero": "COT-003",
            "cliente": "Carlos Martínez",
            "evento": "Cumpleaños",
            "tipo": "Social",
            "fecha": "25/10/2026",
            "hora": "5:00 PM - 9:00 PM",
            "personas": 40,
            "lugar": "Restaurante",
            "estado": "Finalizado",
            "total": 1280.00,
        },
        {
            "numero": "COT-004",
            "cliente": "Ana Rodríguez",
            "evento": "Graduación",
            "tipo": "Graduación",
            "fecha": "02/11/2026",
            "hora": "3:00 PM - 8:00 PM",
            "personas": 65,
            "lugar": "Salón Las Orquídeas",
            "estado": "Pendiente",
            "total": 2750.00,
        },
        {
            "numero": "COT-005",
            "cliente": "Corporación XYZ",
            "evento": "Conferencia empresarial",
            "tipo": "Corporativo",
            "fecha": "08/11/2026",
            "hora": "8:00 AM - 2:00 PM",
            "personas": 120,
            "lugar": "Terraza Secundaria",
            "estado": "Confirmado",
            "total": 4200.00,
        },
        {
            "numero": "COT-006",
            "cliente": "Sofía Hernández",
            "evento": "Baby Shower",
            "tipo": "Social",
            "fecha": "14/11/2026",
            "hora": "2:00 PM - 6:00 PM",
            "personas": 35,
            "lugar": "Restaurante",
            "estado": "Cancelado",
            "total": 950.00,
        },
    ]

    context = {
        "eventos": eventos,

        "total_eventos": len(eventos),

        "pendientes": sum(
            1 for evento in eventos
            if evento["estado"] == "Pendiente"
        ),

        "confirmados": sum(
            1 for evento in eventos
            if evento["estado"] == "Confirmado"
        ),

        "finalizados": sum(
            1 for evento in eventos
            if evento["estado"] == "Finalizado"
        ),
    }

    return render(
        request,
        "EventosHome.html",
        context
    )