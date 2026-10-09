import json

from decimal import Decimal, InvalidOperation

from django.shortcuts import render, redirect

from django.http import JsonResponse

from django.db import transaction

from django.utils import timezone

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import (

    Clientes,

    Eventos,

    Cotizaciones,

    DetalleCotizacion,

    EstadosEvento,

    Pagos,

    TiposEvento,

    Servicios,

    ElementosMontaje,

    PaquetesEvento,

    AreasEvento,

    Platillo,

    Bebidas,

    ServiciosOpcionales,

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

    paquetes_db = (

        PaquetesEvento.objects

        .all()

        .order_by("nombre")

    )

    paquetes = []

    for paquete in paquetes_db:

        servicios_db = (

            Servicios.objects

            .filter(id_paquete=paquete.id_paquete, estado=True)

            .order_by("nombre")

        )

        servicios = []

        for servicio in servicios_db:

            servicios.append({

                "id": str(servicio.id_servicio),

                "nombre": servicio.nombre,

                "descripcion": servicio.descripcion or "",

                "precio": float(servicio.precio or 0),

            })

        paquetes.append({

            "id": str(paquete.id_paquete),

            "nombre": paquete.nombre,

            "subtitulo": paquete.modalidad_pago or "",

            "descripcion": paquete.descripcion or "",

            "min_personas": paquete.min_personas or 0,

            "precio": 0,

            "tipo_precio": "consumo",

            "servicios": servicios,

            "productos": [],

            "montajes": [],

            "nota": paquete.que_incluye or "",

            "incluye": [

                servicio["nombre"]

                for servicio in servicios

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

    if request.method == "POST":

        try:

            data = json.loads(request.body.decode("utf-8"))

            cliente_nombre = (data.get("cliente") or "").strip()

            telefono = (data.get("telefono") or "").strip()

            correo = (data.get("correo") or "").strip()

            tipo_nombre = (data.get("tipo_evento") or "").strip()

            fecha_evento = data.get("fecha_evento")

            hora_inicio = data.get("hora_inicio") or None

            hora_fin = data.get("hora_fin") or None

            lugar_nombre = (data.get("lugar") or "").strip()

            observaciones = (data.get("observaciones") or "").strip()

            personas = int(data.get("personas") or 0)

            conceptos = data.get("conceptos") or []

            paquete_id = str(data.get("paquete_id") or "")

            descuento = Decimal(str(data.get("descuento") or "0"))

            porcentaje_propina = Decimal(

                str(data.get("porcentaje_propina") or "0")

            )

            if not all([

                cliente_nombre,

                tipo_nombre,

                fecha_evento,

                lugar_nombre,

                paquete_id

            ]):

                return JsonResponse({

                    "ok": False,

                    "error": "Completa los datos del cliente, evento, lugar y paquete."

                }, status=400)

            if personas < 1:

                return JsonResponse({

                    "ok": False,

                    "error": "La cantidad de invitados debe ser mayor que cero."

                }, status=400)

            if descuento < 0 or porcentaje_propina < 0:

                return JsonResponse({

                    "ok": False,

                    "error": "Los importes no pueden ser negativos."

                }, status=400)

            tipo_evento = TiposEvento.objects.get(

                nombre=tipo_nombre,

                estado=True

            )

            area = AreasEvento.objects.get(

                nombre=lugar_nombre,

                estado=True

            )

            estado_evento = EstadosEvento.objects.get(

                nombre__iexact="Pendiente"

            )

            # Preparar los detalles de la cotización

            subtotal = Decimal("0.00")

            detalles = []

            for item in conceptos:

                nombre = str(item.get("nombre") or "").strip()

                unidad = str(item.get("unidad") or "unidad")[:50]

                cantidad = Decimal(str(item.get("cantidad") or "1"))

                precio = Decimal(str(item.get("precio") or "0"))

                tipo = str(item.get("tipo") or "")

                if not nombre or cantidad <= 0 or precio < 0:

                    return JsonResponse({

                        "ok": False,

                        "error": "Hay un concepto con datos inválidos."

                    }, status=400)

                importe = (cantidad * precio).quantize(

                    Decimal("0.01")

                )

                subtotal += importe

                detalles.append({

                    "nombre": nombre[:250],

                    "tipo": tipo,

                    "unidad": unidad,

                    "cantidad": cantidad,

                    "precio": precio,

                    "subtotal": importe,

                })

            # Paquete estándar: $21.50 por persona

            if paquete_id == "4":

                subtotal = (

                    Decimal("21.50") * personas

                ).quantize(Decimal("0.01"))

                detalles = [{

                    "nombre": "Paquete privado estándar",

                    "tipo": "Paquete",

                    "unidad": "persona",

                    "cantidad": Decimal(personas),

                    "precio": Decimal("21.50"),

                    "subtotal": subtotal,

                }]

            descuento = min(descuento, subtotal)

            base = max(subtotal - descuento, Decimal("0.00"))

            # Propina para paquetes por consumo

            if paquete_id in ("2", "3"):

                monto_propina = (

                    base * porcentaje_propina / Decimal("100")

                ).quantize(Decimal("0.01"))

            else:

                porcentaje_propina = Decimal("0.00")

                monto_propina = Decimal("0.00")

            total = base + monto_propina

            # Guardar todo dentro de una transacción

            with transaction.atomic():

                cliente = Clientes.objects.create(

                    nombre=cliente_nombre,

                    telefono=telefono or None,

                    correo=correo or None,

                    direccion="",

                    observaciones="",

                    fecha_registro=timezone.now(),

                )

                evento = Eventos.objects.create(

                    cliente=cliente,

                    tipo_evento=tipo_evento,

                    area=area,

                    estado=estado_evento,

                    fecha_evento=fecha_evento,

                    hora_inicio=hora_inicio,

                    hora_fin=hora_fin,

                    hora_inicio_montaje=None,

                    cantidad_adultos=personas,

                    cantidad_ninos=0,

                    total_invitados=personas,

                    observaciones=observaciones,

                    fecha_creacion=timezone.now(),

                )

                ultimo = Cotizaciones.objects.order_by(

                    "-cotizacion_id"

                ).first()

                consecutivo = (

                    ultimo.cotizacion_id + 1

                    if ultimo else 1

                )

                numero = (

                    f"COT-{timezone.localdate().year}-{consecutivo:04d}"

                )

                while Cotizaciones.objects.filter(

                    numero_cotizacion=numero

                ).exists():

                    consecutivo += 1

                    numero = (

                        f"COT-{timezone.localdate().year}-{consecutivo:04d}"

                    )

                cotizacion = Cotizaciones.objects.create(

                    evento=evento,

                    numero_cotizacion=numero,

                    fecha=timezone.localdate(),

                    subtotal=subtotal,

                    porcentaje_propina=porcentaje_propina,

                    monto_propina=monto_propina,

                    descuento=descuento,

                    total=total,

                    estado="Pendiente",

                    observaciones=(

                        f"Paquete seleccionado: "

                        f"{data.get('paquete_nombre', '')}. "

                        f"{observaciones}"

                    ).strip(),

                    fecha_creacion=timezone.now(),

                )

                for detalle in detalles:

                    DetalleCotizacion.objects.create(

                        cotizacion=cotizacion,

                        producto_evento_id=None,

                        elemento_montaje=None,

                        concepto=detalle["nombre"],

                        descripcion=detalle["tipo"],

                        cantidad=detalle["cantidad"],

                        unidad=detalle["unidad"],

                        precio_unitario=detalle["precio"],

                        subtotal=detalle["subtotal"],

                        observaciones="",

                    )

            return JsonResponse({

                "ok": True,

                "numero_cotizacion": numero,

                "total": str(total),

                "mensaje": "Cotización guardada correctamente."

            })

        except TiposEvento.DoesNotExist:

            return JsonResponse({

                "ok": False,

                "error": "El tipo de evento seleccionado no existe o está inactivo."

            }, status=400)

        except AreasEvento.DoesNotExist:

            return JsonResponse({

                "ok": False,

                "error": "El lugar seleccionado no existe o está inactivo."

            }, status=400)

        except EstadosEvento.DoesNotExist:

            return JsonResponse({

                "ok": False,

                "error": "No existe el estado de evento Pendiente en la base de datos."

            }, status=400)

        except (ValueError, InvalidOperation, TypeError):

            return JsonResponse({

                "ok": False,

                "error": "Revisa los números, la fecha y los datos ingresados."

            }, status=400)

        except Exception as error:

            return JsonResponse({

                "ok": False,

                "error": str(error)

            }, status=500)

    # GET: mostrar el formulario

    # GET: mostrar el formulario y cargar el catálogo

    import json

    areas = AreasEvento.objects.filter(

        estado=True

    ).order_by("nombre")

    tipos_evento = TiposEvento.objects.filter(

        estado=True

    ).order_by("nombre")

    platillos = Platillo.objects.all().order_by("nombre")

    bebidas = Bebidas.objects.all().order_by("nombre")

    servicios = Servicios.objects.filter(

        estado=True

    ).order_by("nombre")

    servicios_opcionales = ServiciosOpcionales.objects.all()

    # Preparar el catálogo que utiliza cotizacionNueva.html

    catalogo = []

    for platillo in platillos:

        catalogo.append({

            "id": platillo.pk,

            "nombre": platillo.nombre,

            "tipo": (

                str(platillo.categoria.nombre)

                if getattr(platillo, "categoria", None)

                else "Platillo"

            ),

            "precio": platillo.precio or 0,

            "unidad": "persona",

        })

    for bebida in bebidas:

        catalogo.append({

            "id": bebida.pk,

            "nombre": bebida.nombre,

            "tipo": (

                str(bebida.categoria.nombre)

                if getattr(bebida, "categoria", None)

                else "Bebida"

            ),

            "precio": bebida.precio or 0,

            "unidad": "persona",

        })

    for servicio in servicios:

        catalogo.append({

            "id": servicio.pk,

            "nombre": servicio.nombre,

            "tipo": "Servicio",

            "precio": servicio.precio or 0,

            "unidad": "evento",

        })

    # Preparar los servicios opcionales

    variables = []

    for item in servicios_opcionales:

        variables.append({

            "id": item.pk,

            "nombre": item.nombre,

            "descripcion": getattr(item, "descripcion", "") or "",

            "precio": getattr(item, "precio", 0) or 0,

            "unidad": getattr(item, "unidad", None) or "evento",

        })

    # Categorías disponibles para el filtro del catálogo

    categorias = sorted({

        item["tipo"] for item in catalogo

    })

    # Obtener los paquetes una sola vez

    paquetes = obtener_paquetes()

    # Preparar opciones para los select del HTML

    lugares = list(

        areas.values_list("nombre", flat=True)

    )

    tipos_evento_lista = list(

        tipos_evento.values_list("nombre", flat=True)

    )

    context = {

        "areas": areas,

        "lugares": lugares,

        "tipos_evento": tipos_evento_lista,

        "platillos": platillos,

        "bebidas": bebidas,

        "servicios": servicios,

        "servicios_opcionales": servicios_opcionales,

        "catalogo": catalogo,

        "variables": variables,

        "categorias": categorias,

        "paquetes": paquetes,

        "paquetes_json": json.dumps(

            paquetes,

            default=str,

            ensure_ascii=False

        ),

    }

    return render(request, "cotizacionNueva.html", context)

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
