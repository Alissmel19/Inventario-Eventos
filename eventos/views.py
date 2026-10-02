from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import (
    Clientes,
    Eventos,
    Cotizaciones,
    Pagos,
    TiposEvento,
    ProductosEvento,
    Servicios,
    ElementosMontaje,
    PaquetesEvento,
    AreasEvento,
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
                "error": "Usuario o contraseÃ±a incorrectos."
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
# CERRAR SESIÃ“N
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
            "cliente": "MarÃa LÃ³pez",
            "evento": "Boda",
            "tipo": "Boda",
            "fecha": "15/10/2026",
            "hora": "4:00 PM - 9:00 PM",
            "personas": 50,
            "lugar": "SalÃ³n VIP",
            "estado": "Pendiente",
            "total": 2131.25,
            "paquete": "Paquete VIP",
            "telefono": "7123-4567",
            "correo": "maria@email.com",
            "observaciones": "Ceremonia en jardÃn.",
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
            "cliente": "Carlos MartÃnez",
            "evento": "CumpleaÃ±os",
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
            "observaciones": "CelebraciÃ³n familiar.",
        },

        {
            "numero": "COT-004",
            "cliente": "Ana RodrÃguez",
            "evento": "GraduaciÃ³n",
            "tipo": "GraduaciÃ³n",
            "fecha": "02/11/2026",
            "hora": "3:00 PM - 8:00 PM",
            "personas": 65,
            "lugar": "SalÃ³n Las OrquÃdeas",
            "estado": "Pendiente",
            "total": 2750.00,
            "paquete": "Evento por Consumo + SalÃ³n Las OrquÃdeas",
            "telefono": "7456-7890",
            "correo": "ana@email.com",
            "observaciones": "Se requiere proyector.",
        },

        {
            "numero": "COT-005",
            "cliente": "CorporaciÃ³n XYZ",
            "evento": "Conferencia empresarial",
            "tipo": "Corporativo",
            "fecha": "08/11/2026",
            "hora": "8:00 AM - 2:00 PM",
            "personas": 120,
            "lugar": "Terraza Secundaria",
            "estado": "Confirmado",
            "total": 4200.00,
            "paquete": "Evento por Consumo + SalÃ³n Las OrquÃdeas",
            "telefono": "2222-3333",
            "correo": "eventos@xyz.com",
            "observaciones": "Evento empresarial.",
        },

        {
            "numero": "COT-006",
            "cliente": "SofÃa HernÃ¡ndez",
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

    paquetes_db = (
        PaquetesEvento.objects
        .filter(activo=True)
        .select_related("tipo_evento")
        .prefetch_related(
            "productos__producto__categoria",
            "servicios__servicio",
            "montajes__elemento",
        )
        .order_by("nombre")
    )

    paquetes = []

    for paquete in paquetes_db:
        productos = []
        servicios = []
        montajes = []

        for item in paquete.productos.all():
            productos.append({
                "nombre": item.producto.nombre,
                "cantidad": float(item.cantidad or 0)
            })

        for item in paquete.servicios.all():
            servicios.append({
                "nombre": item.servicio.nombre,
                "cantidad": float(item.cantidad or 0)
            })

        for item in paquete.montajes.all():
            montajes.append({
                "nombre": item.elemento.nombre,
                "cantidad": float(item.cantidad or 0)
            })

        if paquete.precio_base == 0:
            precio = 0
            tipo_precio = "consumo"
        else:
            precio = float(paquete.precio_base)
            # Los paquetes VIP/infantil se cobran por persona;
            # los demás paquetes con monto base se cobran por evento.
            nombre_lower = paquete.nombre.lower()
            tipo_precio = "persona" if (
                "vip" in nombre_lower or
                "infantil" in nombre_lower
            ) else "fijo"

        nota = ""
        if tipo_precio == "consumo":
            nota = "Consumo según los alimentos y bebidas seleccionados."
        elif tipo_precio == "persona":
            nota = "Precio base por persona. La cantidad se actualiza con el número de invitados."
        else:
            nota = "Precio base por evento."

        paquetes.append({
            "id": str(paquete.id_paquete),
            "nombre": paquete.nombre,
            "subtitulo": paquete.tipo_evento.nombre,
            "descripcion": paquete.descripcion or "",
            "precio": precio,
            "tipo_precio": tipo_precio,
            "productos": productos,
            "servicios": servicios,
            "montajes": montajes,
            "nota": nota,
            "incluye": [
                item["nombre"]
                for item in productos + servicios + montajes
            ],
        })

    return paquetes


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
# NUEVA COTIZACIÃ“N
# ============================================================

@login_required(login_url="login")
def nueva_cotizacion(request):

    import json

    lugares = list(
        AreasEvento.objects
        .filter(estado=True)
        .values_list("nombre", flat=True)
    )

    tipos_evento = list(
        TiposEvento.objects
        .filter(estado=True)
        .values_list("nombre", flat=True)
        .order_by("nombre")
    )

    productos_db = (
        ProductosEvento.objects
        .filter(estado=True)
        .select_related("categoria")
        .order_by("nombre")
    )

    catalogo = []

    for producto in productos_db:
        catalogo.append({
            "id": producto.producto_evento_id,
            "nombre": producto.nombre,
            "tipo": producto.categoria.nombre if producto.categoria else "Sin categoría",
            "precio": float(producto.precio_base or 0),
            "unidad": producto.unidad_medida,
        })

    servicios_db = (
        Servicios.objects
        .filter(estado=True)
        .order_by("nombre")
    )

    variables = []

    for servicio in servicios_db:
        variables.append({
            "id": servicio.servicio_id,
            "nombre": servicio.nombre,
            "descripcion": servicio.descripcion or "",
            "precio": float(servicio.precio_base or 0),
            "unidad": "evento",
        })

    categorias = list(dict.fromkeys(item["tipo"] for item in catalogo))
    paquetes = obtener_paquetes()

    context = {
        "lugares": lugares,
        "tipos_evento": tipos_evento,
        "catalogo": catalogo,
        "variables": variables,
        "categorias": categorias,
        "paquetes": paquetes,
        "paquetes_json": json.dumps(paquetes, ensure_ascii=False),
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
            "cliente": "MarÃa LÃ³pez",
            "evento": "Boda",
            "tipo": "Boda",
            "fecha": "15/10/2026",
            "hora": "4:00 PM - 9:00 PM",
            "personas": 50,
            "lugar": "SalÃ³n VIP",
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
            "cliente": "Carlos MartÃnez",
            "evento": "CumpleaÃ±os",
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
            "cliente": "Ana RodrÃguez",
            "evento": "GraduaciÃ³n",
            "tipo": "GraduaciÃ³n",
            "fecha": "02/11/2026",
            "hora": "3:00 PM - 8:00 PM",
            "personas": 65,
            "lugar": "SalÃ³n Las OrquÃdeas",
            "estado": "Pendiente",
            "total": 2750.00,
        },
        {
            "numero": "COT-005",
            "cliente": "CorporaciÃ³n XYZ",
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
            "cliente": "SofÃa HernÃ¡ndez",
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
