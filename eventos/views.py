import json
import uuid
from datetime import datetime
from decimal import Decimal, InvalidOperation
from django.db.models import Sum, Q
from collections import Counter
from decimal import Decimal, InvalidOperation
import os
from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal, ROUND_DOWN
from .models import RestriccionesCotizacion
from django.conf import settings
from reportlab.platypus import Image
from django.http import JsonResponse

from django.db import transaction

from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import HabitacionesUnidades, DetalleHospedaje


from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError

from io import BytesIO
from xml.sax.saxutils import escape

from django.http import HttpResponse
from django.contrib import messages
from django.db import transaction
from django.utils import timezone

from .models import ReservaHabitacionWeb

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)



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
    Hospedaje,
    HabitacionesUnidades,
    DetalleHospedaje,
    MetodosPago,

    Cotizaciones, Eventos, Clientes, 
    Pagos,
    SubpaquetesEvento,
    PaqueteConceptos,
    SubpaqueteConceptos,
    RestriccionesCotizacion

    

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

# DASHBOARD GENERAL DaSGOEN 

# ============================================================

def dashboard(request):
    hoy = timezone.localdate()
    anio = hoy.year
    mes = hoy.month

    # Cotizaciones creadas durante el mes actual
    cotizaciones_mes = Cotizaciones.objects.filter(
        fecha_creacion__year=anio,
        fecha_creacion__month=mes
    ).count()

    # Eventos confirmados según el estado de su cotización
    estados_aceptados = [
        "aceptada",
        "aceptado",
        "confirmada",
        "confirmado",
    ]

    eventos_confirmados = (
        Cotizaciones.objects
        .filter(
            estado__iregex=r"^(aceptada|aceptado|confirmada|confirmado)$",
            evento__isnull=False,
        )
        .values("evento_id")
        .distinct()
        .count()
    )

    # Total de clientes registrados
    total_clientes = Clientes.objects.count()

    # Total de pagos registrados
    ingresos = (
        Pagos.objects.aggregate(total=Sum("monto"))["total"]
        or 0
    )

    # Cotizaciones más recientes
    cotizaciones_recientes = (
        Cotizaciones.objects
        .select_related("evento__cliente")
        .order_by("-fecha_creacion")[:5]
    )

    # Eventos por mes del año actual
    fechas_eventos = Eventos.objects.filter(
        fecha_evento__year=anio
    ).values_list("fecha_evento", flat=True)

    conteo_meses = Counter(
        fecha.month for fecha in fechas_eventos
    )

    eventos_por_mes = [
        conteo_meses.get(numero_mes, 0)
        for numero_mes in range(1, 13)
    ]

    context = {
        "total_cotizaciones_mes": cotizaciones_mes,
        "eventos_confirmados": eventos_confirmados,
        "total_clientes": total_clientes,
        "ingresos_registrados": ingresos,
        "cotizaciones_recientes": cotizaciones_recientes,
        "eventos_por_mes": eventos_por_mes,
        "anio_actual": anio,
    }

    return render(request, "dashboard.html", context)
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
    paquetes = []

    paquetes_db = PaquetesEvento.objects.all().order_by("nombre")

    for paquete in paquetes_db:
        # Categorías de platillos permitidas para este paquete.
        categorias_platillos = set()

        conceptos_db = (
            PaqueteConceptos.objects
            .filter(paquete_id=paquete.id_paquete)
            .select_related(
                "platillo",
                "bebida",
                "servicio",
                "servicio_opcional",
                "elemento_montaje",
                "area",
            )
        )

        conceptos = []

        for concepto in conceptos_db:
            if concepto.platillo_id:
                if concepto.platillo.categoria_id:
                    categorias_platillos.add(concepto.platillo.categoria_id)
                conceptos.append({
                    "id": concepto.platillo_id,
                    "categoria_id": concepto.platillo.categoria_id,
                    "nombre": concepto.platillo.nombre,
                    "grupo": "platillo",
                    "precio": float(
                        concepto.precio_aplicado
                        or concepto.platillo.precio
                        or 0
                    ),
                    "cantidad": float(concepto.cantidad or 0),
                    "obligatorio": concepto.obligatorio,
                })

            elif concepto.bebida_id:
                conceptos.append({
                    "id": concepto.bebida_id,
                    "nombre": concepto.bebida.nombre,
                    "grupo": "bebida",
                    "precio": float(
                        concepto.precio_aplicado
                        or concepto.bebida.precio
                        or 0
                    ),
                    "cantidad": float(concepto.cantidad or 0),
                    "obligatorio": concepto.obligatorio,
                })

            elif concepto.servicio_id:
                conceptos.append({
                    "id": concepto.servicio_id,
                    "nombre": concepto.servicio.nombre,
                    "grupo": "servicio",
                    "precio": float(
                        concepto.precio_aplicado
                        or concepto.servicio.precio
                        or 0
                    ),
                    "cantidad": float(concepto.cantidad or 0),
                    "obligatorio": concepto.obligatorio,
                })

            elif concepto.servicio_opcional_id:
                conceptos.append({
                    "id": concepto.servicio_opcional_id,
                    "nombre": concepto.servicio_opcional.nombre,
                    "grupo": "servicio_opcional",
                    "precio": float(
                        concepto.precio_aplicado
                        or concepto.servicio_opcional.precio
                        or 0
                    ),
                    "cantidad": float(concepto.cantidad or 0),
                    "obligatorio": concepto.obligatorio,
                })

            elif concepto.elemento_montaje_id:
                conceptos.append({
                    "id": concepto.elemento_montaje_id,
                    "nombre": concepto.elemento_montaje.nombre,
                    "grupo": "montaje",
                    "precio": float(
                        concepto.precio_aplicado
                        or concepto.elemento_montaje.precio
                        or 0
                    ),
                    "cantidad": float(concepto.cantidad or 0),
                    "obligatorio": concepto.obligatorio,
                })

        subpaquetes = []

        subpaquetes_db = (
            SubpaquetesEvento.objects
            .filter(paquete_id=paquete.id_paquete, activo=True)
            .order_by("nombre")
        )

        for subpaquete in subpaquetes_db:
            conceptos_sub = (
                SubpaqueteConceptos.objects
                .filter(subpaquete_id=subpaquete.id_subpaquete)
                .select_related(
                    "platillo",
                    "bebida",
                    "servicio",
                    "servicio_opcional",
                    "elemento_montaje",
                )
            )

            opciones = []

            for concepto in conceptos_sub:
                if concepto.platillo_id:
                    if concepto.platillo.categoria_id:
                        categorias_platillos.add(concepto.platillo.categoria_id)
                    opciones.append({
                        "id": concepto.platillo_id,
                        "categoria_id": concepto.platillo.categoria_id,
                        "nombre": concepto.platillo.nombre,
                        "grupo": "platillo",
                        "precio": float(
                            concepto.precio_unitario
                            or concepto.platillo.precio
                            or 0
                        ),
                        "cantidad": float(concepto.cantidad or 0),
                        "obligatorio": concepto.obligatorio,
                        "cortesia": concepto.es_cortesia,
                    })

                elif concepto.bebida_id:
                    opciones.append({
                        "id": concepto.bebida_id,
                        "nombre": concepto.bebida.nombre,
                        "grupo": "bebida",
                        "precio": float(
                            concepto.precio_unitario
                            or concepto.bebida.precio
                            or 0
                        ),
                        "cantidad": float(concepto.cantidad or 0),
                        "obligatorio": concepto.obligatorio,
                        "cortesia": concepto.es_cortesia,
                    })

                elif concepto.servicio_id:
                    opciones.append({
                        "id": concepto.servicio_id,
                        "nombre": concepto.servicio.nombre,
                        "grupo": "servicio",
                        "precio": float(
                            concepto.precio_unitario
                            or concepto.servicio.precio
                            or 0
                        ),
                        "cantidad": float(concepto.cantidad or 0),
                        "obligatorio": concepto.obligatorio,
                        "cortesia": concepto.es_cortesia,
                    })

                elif concepto.servicio_opcional_id:
                    opciones.append({
                        "id": concepto.servicio_opcional_id,
                        "nombre": concepto.servicio_opcional.nombre,
                        "grupo": "servicio_opcional",
                        "precio": float(
                            concepto.precio_unitario
                            or concepto.servicio_opcional.precio
                            or 0
                        ),
                        "cantidad": float(concepto.cantidad or 0),
                        "obligatorio": concepto.obligatorio,
                        "cortesia": concepto.es_cortesia,
                    })

                elif concepto.elemento_montaje_id:
                    opciones.append({
                        "id": concepto.elemento_montaje_id,
                        "nombre": concepto.elemento_montaje.nombre,
                        "grupo": "montaje",
                        "precio": float(
                            concepto.precio_unitario
                            or concepto.elemento_montaje.precio
                            or 0
                        ),
                        "cantidad": float(concepto.cantidad or 0),
                        "obligatorio": concepto.obligatorio,
                        "cortesia": concepto.es_cortesia,
                    })

            subpaquetes.append({
                "id": str(subpaquete.id_subpaquete),
                "nombre": subpaquete.nombre,
                "descripcion": subpaquete.descripcion or "",
                "conceptos": opciones,
            })

        # IDs exactos de platillos asignados al paquete y a sus subpaquetes.
        # El catálogo se filtra por estos IDs, no por categoría.
        platillos_permitidos = sorted({
            int(item["id"])
            for item in conceptos
            if item.get("grupo") == "platillo"
        } | {
            int(item["id"])
            for subpaquete in subpaquetes
            for item in subpaquete.get("conceptos", [])
            if item.get("grupo") == "platillo"
        })

        paquetes.append({
            "id": str(paquete.id_paquete),
            "nombre": paquete.nombre,
            "subtitulo": paquete.modalidad_pago or "",
            "descripcion": paquete.descripcion or "",
            "min_personas": paquete.min_personas or 0,
            "precio": 0,
            "tipo_precio": "consumo",
            "conceptos": conceptos,
            "subpaquetes": subpaquetes,
            "categorias_platillos": sorted(categorias_platillos),
            "platillos_permitidos": platillos_permitidos,
            "servicios": [],
            "productos": [],
            "montajes": [],
            "nota": paquete.que_incluye or "",
            "incluye": [c["nombre"] for c in conceptos],
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

            # Validar que la hora final sea posterior a la inicial
            if hora_inicio and hora_fin:
                hora_inicio_obj = datetime.strptime(hora_inicio, "%H:%M").time()
                hora_fin_obj = datetime.strptime(hora_fin, "%H:%M").time()

                if hora_inicio_obj >= hora_fin_obj:
                    return JsonResponse({
                        "ok": False,
                        "error": "La hora de finalización debe ser posterior a la hora de inicio."
                    }, status=400)

            lugar_nombre = (data.get("lugar") or "").strip()

            observaciones = (data.get("observaciones") or "").strip()

            personas = int(data.get("personas") or 0)

            cantidad_ninos = int(data.get("cantidad_ninos") or 0)

            if personas < 1 or cantidad_ninos < 0:
                return JsonResponse({
                    "ok": False,
                    "error": "La cantidad de personas debe ser mayor a cero y los niños no pueden ser negativos."
                }, status=400)

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
            subtotal_consumo = Decimal("0.00")
            detalles = []

            
            for item in conceptos:
                nombre = str(item.get("nombre") or "").strip()
                unidad = str(item.get("unidad") or "unidad")[:50]
                cantidad = Decimal(str(item.get("cantidad") or "1"))
                precio = Decimal(str(item.get("precio") or "0"))
                tipo = str(item.get("tipo") or "")
                incluido = item.get("incluido") is True

                if not nombre or cantidad <= 0 or precio < 0:
                    return JsonResponse({
                        "ok": False,
                        "error": "Hay un concepto con datos inválidos."
                    }, status=400)

                # Los conceptos incluidos forman parte del paquete; no deben
                # guardarse como servicios adicionales individuales.
                if incluido:
                    continue

                importe = (cantidad * precio).quantize(Decimal("0.01"))
                subtotal += importe

                # Solo platillos y bebidas generan propina.
                tipo_normalizado = tipo.strip().lower()
                if tipo_normalizado in ("platillo", "bebida"):
                    subtotal_consumo += importe

                detalles.append({
                    "nombre": nombre[:250],
                    "tipo": tipo,
                    "unidad": unidad,
                    "cantidad": cantidad,
                    "precio": precio,
                    "subtotal": importe,
                })
           
            # Aplicar el porcentaje de propina ingresado
# sobre el subtotal de la cotización.
            base_propina = max(
                subtotal - descuento,
                Decimal("0.00"),
            )

            monto_propina = (
                base_propina
                * porcentaje_propina
                / Decimal("100")
            ).quantize(Decimal("0.01"))

            # El descuento se aplica al subtotal general.
            base = max(
                subtotal - descuento,
                Decimal("0.00"),
            )

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

                estado_evento = EstadosEvento.objects.get(
                    nombre__iexact="Pendiente"
                )

                # Validar que no exista otro evento en la misma fecha y lugar.
                evento_existente = Eventos.objects.filter(
                    fecha_evento=fecha_evento,
                    area=area,
                ).exclude(
                    estado__nombre__iexact="Cancelado"
                ).exists()

                if evento_existente:
                    return JsonResponse({
                        "ok": False,
                        "error": (
                            "Ya existe un evento reservado en este lugar "
                            "para la fecha seleccionada. Elige otra fecha o lugar."
                        )
                    }, status=400)

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

                    cantidad_ninos=cantidad_ninos,
                    
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

                    estado="Borrador",

                    observaciones=(
                        f"Paquete seleccionado: {str(data.get('paquete_nombre', '')).strip()}. "
                        f"{observaciones}\n\n"
                        "[[PAQUETE_META]]"
                        + json.dumps({
                            "paquete_id": paquete_id,
                            "paquete_nombre": str(data.get("paquete_nombre") or "").strip(),
                            "subpaquete_id": str(data.get("subpaquete_id") or "").strip(),
                            "subpaquete_nombre": str(data.get("subpaquete_nombre") or "").strip(),
                        }, ensure_ascii=False)
                    ).strip(),

                    fecha_creacion=timezone.now(),

                )

                
                for detalle in detalles:
                    tipo_concepto = str(detalle.get("tipo", "")).strip().lower()

                    # Por ahora, solo vinculamos elementos de montaje
                    # cuando tengamos confirmado su ID real.
                    elemento_montaje = None

                    DetalleCotizacion.objects.create(
                        cotizacion=cotizacion,
                        producto_evento_id=None,
                        elemento_montaje=elemento_montaje,
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

        except (ValueError, InvalidOperation, TypeError) as error:
            import logging
            logging.exception("Error de validación al guardar cotización")

            return JsonResponse({
                "ok": False,
                "error": f"{type(error).__name__}: {str(error)}"
            }, status=400)
        except Exception as error:
            import logging
            logging.exception("ERROR COMPLETO AL GUARDAR COTIZACION")

            return JsonResponse({
                "ok": False,
                "error": str(error)
            }, status=500)

    # GET: mostrar el formulario

    # GET: mostrar el formulario y cargar el catálogo

  

    areas = AreasEvento.objects.filter(

        estado=True

    ).order_by("nombre")

    tipos_evento = TiposEvento.objects.filter(

        estado=True

    ).order_by("nombre")

    platillos = Platillo.objects.all().order_by("nombre")

    bebidas = Bebidas.objects.all().order_by("nombre")
    # El filtro contempla categorías de platillos y bebidas.
    categorias = sorted({
        str(item.categoria.nombre).strip()
        for item in list(platillos) + list(bebidas)
        if getattr(item, "categoria", None) and item.categoria.nombre
    } | {"Servicio"})

    servicios = Servicios.objects.filter(

        estado=True

    ).order_by("nombre")

    servicios_opcionales = ServiciosOpcionales.objects.all()

    # Preparar el catálogo que utiliza cotizacionNueva.html

    catalogo = []

    for platillo in platillos:
        catalogo.append({
            "id": platillo.pk,
            "grupo": "platillo",
            "categoria_id": platillo.categoria_id,
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
            "grupo": "bebida",
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
            "grupo": "servicio",
            "nombre": servicio.nombre,
            "tipo": "Servicio",
            "precio": servicio.precio or 0,
            "unidad": "evento",
        })    # Preparar los servicios opcionales
    # Preparar los servicios opcionales
    variables = []

    for item in servicios_opcionales:
        variables.append({
            "id": item.pk,
            "nombre": item.nombre,
            "grupo": "servicio",
            "precio": float(item.precio or 0),
            "unidad": "evento",
        })

    # Obtener los paquetes una sola vez
    paquetes = obtener_paquetes()
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

        "cotizacionNueva.html",

        context

    )




@login_required(login_url="login")
@require_GET
def habitaciones_disponibles(request):
    fecha_entrada = parse_date(
        request.GET.get("fecha_entrada", "")
    )
    fecha_salida = parse_date(
        request.GET.get("fecha_salida", "")
    )

    if not fecha_entrada or not fecha_salida:
        return JsonResponse({
            "ok": False,
            "error": "Ingresá las fechas de entrada y salida."
        }, status=400)

    if fecha_salida <= fecha_entrada:
        return JsonResponse({
            "ok": False,
            "error": "La salida debe ser posterior a la entrada."
        }, status=400)

    # Buscar habitaciones ocupadas por reservas aceptadas
    ocupadas = DetalleHospedaje.objects.filter(
        fecha_check_in__lt=fecha_salida,
        fecha_check_out__gt=fecha_entrada,
        id_unidad__isnull=False,
        id_hospedaje__cotizacion__estado="Aceptada",
    ).values_list("id_unidad_id", flat=True)

    disponibles = (
        HabitacionesUnidades.objects
        .filter(activa=True)
        .exclude(id_unidad__in=ocupadas)
        .select_related("id_habitaciones")
        .order_by("id_unidad")
    )

    habitaciones = [
        {
            "id_unidad": unidad.id_unidad,
            "nombre": unidad.nombre_unidad,
            "tipo": unidad.id_habitaciones.nombre,
            "capacidad": unidad.id_habitaciones.capacidad,
            "precio_noche": str(unidad.id_habitaciones.precio),
        }
        for unidad in disponibles
    ]

    return JsonResponse({
        "ok": True,
        "fecha_entrada": fecha_entrada.isoformat(),
        "fecha_salida": fecha_salida.isoformat(),
        "total_disponibles": len(habitaciones),
        "habitaciones": habitaciones,
    })



@login_required(login_url="login")
def cotizar_hospedaje(request):
    return render(request, "cotizar_hospedaje.html")

@login_required(login_url="login")
@require_GET
def calendario_hospedaje(request):
    anio = int(request.GET.get("anio", timezone.localdate().year))
    mes = int(request.GET.get("mes", timezone.localdate().month))

    if mes < 1 or mes > 12:
        return JsonResponse({
            "ok": False,
            "error": "Mes inválido."
        }, status=400)

    desde = date(anio, mes, 1)

    if mes == 12:
        hasta = date(anio + 1, 1, 1)
    else:
        hasta = date(anio, mes + 1, 1)

    unidades = (
        HabitacionesUnidades.objects
        .filter(activa=True)
        .select_related("id_habitaciones")
        .order_by("id_unidad")
    )

    reservas = (
        DetalleHospedaje.objects
        .filter(
            fecha_check_in__lt=hasta,
            fecha_check_out__gt=desde,
            id_hospedaje__cotizacion__estado="Aceptada"
        )
        .select_related(
            "id_unidad",
            "id_habitaciones",
            "id_hospedaje__cliente",
            "id_hospedaje__cotizacion"
        )
        .order_by("fecha_check_in")
    )

    datos_reservas = []

    for detalle in reservas:
        hospedaje = detalle.id_hospedaje
        cliente = hospedaje.cliente
        cotizacion = hospedaje.cotizacion

        pagos = Pagos.objects.filter(
            cotizacion=cotizacion
        ).select_related("metodo_pago")

        formas_pago = list(
            pagos.values_list("metodo_pago__nombre", flat=True).distinct()
        )

        datos_reservas.append({
            "id_detalle": detalle.id_detalle_hospedaje,
            "id_unidad": detalle.id_unidad_id,
            "habitacion": (
                detalle.id_unidad.nombre_unidad
                if detalle.id_unidad else "Sin unidad"
            ),
            "cliente": cliente.nombre if cliente else "",
            "telefono": cliente.telefono if cliente else "",
            "correo": cliente.correo if cliente else "",
            "factura": cotizacion.numero_cotizacion,
            "fecha_reserva": (
                hospedaje.fecha.strftime("%d/%m/%Y")
                if hospedaje.fecha else ""
            ),
            "entrada": (
                detalle.fecha_check_in.isoformat()
                if detalle.fecha_check_in else ""
            ),
            "salida": (
                detalle.fecha_check_out.isoformat()
                if detalle.fecha_check_out else ""
            ),
            "noches": (
                (detalle.fecha_check_out - detalle.fecha_check_in).days
                if detalle.fecha_check_in and detalle.fecha_check_out
                else 0
            ),
            "tarifa": str(
                detalle.precio_unitario
                if detalle.precio_unitario is not None
                else detalle.id_habitaciones.precio
            ),
            "total": str(hospedaje.total or 0),
            "estado": cotizacion.estado,
            "forma_pago": ", ".join(formas_pago) if formas_pago else "Pendiente",
            "observaciones": cotizacion.observaciones or "",
        })

    datos_unidades = [
        {
            "id": unidad.id_unidad,
            "nombre": unidad.nombre_unidad,
            "tipo": unidad.id_habitaciones.nombre,
            "capacidad": unidad.id_habitaciones.capacidad,
            "precio": str(unidad.id_habitaciones.precio or 0),
        }
        for unidad in unidades
    ]

    return JsonResponse({
        "ok": True,
        "anio": anio,
        "mes": mes,
        "unidades": datos_unidades,
        "reservas": datos_reservas,
    })

@login_required(login_url="login")
@require_POST
def guardar_cotizacion_hospedaje(request):
    nombre = request.POST.get("nombre", "").strip()
    telefono = request.POST.get("telefono", "").strip()
    correo = request.POST.get("correo", "").strip()

    fecha_entrada = parse_date(request.POST.get("fecha_entrada", ""))
    fecha_salida = parse_date(request.POST.get("fecha_salida", ""))

    ids_unidades = request.POST.getlist("habitaciones")

    if not nombre:
        return JsonResponse({
            "ok": False,
            "error": "El nombre del cliente es obligatorio."
        }, status=400)

    if not fecha_entrada or not fecha_salida:
        return JsonResponse({
            "ok": False,
            "error": "Debes indicar las fechas de entrada y salida."
        }, status=400)

    if fecha_salida <= fecha_entrada:
        return JsonResponse({
            "ok": False,
            "error": "La salida debe ser posterior a la entrada."
        }, status=400)

    if not ids_unidades:
        return JsonResponse({
            "ok": False,
            "error": "Selecciona al menos una habitación."
        }, status=400)

    try:
        ids_unidades = list({int(valor) for valor in ids_unidades})
    except (ValueError, TypeError):
        return JsonResponse({
            "ok": False,
            "error": "La selección de habitaciones no es válida."
        }, status=400)

    noches = (fecha_salida - fecha_entrada).days

    try:
        with transaction.atomic():
            unidades = list(
                HabitacionesUnidades.objects
                .select_for_update()
                .filter(
                    id_unidad__in=ids_unidades,
                    activa=True
                )
                .select_related("id_habitaciones")
            )

            if len(unidades) != len(ids_unidades):
                return JsonResponse({
                    "ok": False,
                    "error": "Una o más habitaciones no existen o están inactivas."
                }, status=400)

            # Solo las cotizaciones aceptadas bloquean habitaciones.
            ocupadas = DetalleHospedaje.objects.filter(
                fecha_check_in__lt=fecha_salida,
                fecha_check_out__gt=fecha_entrada,
                id_unidad__in=ids_unidades,
                id_hospedaje__cotizacion__estado="Aceptada",
            ).values_list("id_unidad_id", flat=True)

            ids_ocupadas = set(ocupadas)

            if ids_ocupadas:
                return JsonResponse({
                    "ok": False,
                    "error": (
                        "Una o más habitaciones ya están reservadas "
                        "para esas fechas. Consulta la disponibilidad otra vez."
                    )
                }, status=409)

            subtotal = sum(
                (
                    Decimal(str(unidad.id_habitaciones.precio))
                    * noches
                    for unidad in unidades
                ),
                Decimal("0.00")
            )

            ahora = timezone.now()

            cliente = Clientes.objects.create(
                nombre=nombre,
                telefono=telefono or None,
                correo=correo or None,
                fecha_registro=ahora,
            )

            numero = f"HOS-{ahora:%Y%m%d}-{uuid.uuid4().hex[:8].upper()}"

            cotizacion = Cotizaciones.objects.create(
                evento=None,
                numero_cotizacion=numero,
                fecha=ahora.date(),
                subtotal=subtotal,
                porcentaje_propina=Decimal("0.00"),
                monto_propina=Decimal("0.00"),
                descuento=Decimal("0.00"),
                total=subtotal,
                estado="Aceptada",
                observaciones=(
                    f"Cotización independiente de hospedaje. "
                    f"Entrada: {fecha_entrada}; salida: {fecha_salida}; "
                    f"noches: {noches}."
                ),
                fecha_creacion=ahora,
            )

            hospedaje = Hospedaje.objects.create(
                total=subtotal,
                fecha=ahora,
                cliente=cliente,
                cotizacion=cotizacion,
            )

            for unidad in unidades:
                DetalleHospedaje.objects.create(
                    id_hospedaje=hospedaje,
                    id_habitaciones=unidad.id_habitaciones,
                    id_unidad=unidad,
                    fecha_check_in=fecha_entrada,
                    fecha_check_out=fecha_salida,
                    precio_unitario=unidad.id_habitaciones.precio,
                )

        return JsonResponse({
            "ok": True,
            "mensaje": "La cotización se guardó correctamente.",
            "numero_cotizacion": numero,
            "total": str(subtotal),
            "noches": noches,
        })

    except (InvalidOperation, TypeError, ValueError):
        return JsonResponse({
            "ok": False,
            "error": "No se pudo calcular el total. Revisa los precios de las habitaciones."
        }, status=400)

    
    except Exception as error:
        import logging
        logging.exception("Error guardando cotización de hospedaje")

        return JsonResponse({
            "ok": False,
            "error": str(error),
        }, status=500)



@login_required(login_url="/login/")
def formulario_pago(request):
    cotizaciones = (
        Cotizaciones.objects
        .filter(estado="Aceptada")
        .select_related("evento")
        .order_by("-fecha")
    )

    metodos_pago = MetodosPago.objects.filter(
        estado=True
    ).order_by("nombre")

    datos_cotizaciones = []

    for cotizacion in cotizaciones:
        es_hospedaje = Hospedaje.objects.filter(
            cotizacion_id=cotizacion.cotizacion_id
        ).exists()

        categoria = "Hospedaje" if es_hospedaje else "Evento"

        pagos_cotizacion = Pagos.objects.filter(
            cotizacion=cotizacion
        ).exclude(estado_pago="Rechazado")

        total_registrado = sum(
            (pago.monto for pago in pagos_cotizacion),
            Decimal("0.00")
        )

        total_aprobado = sum(
            (
                pago.monto
                for pago in pagos_cotizacion
                if pago.estado_pago == "Aprobado"
            ),
            Decimal("0.00")
        )

        total_pendiente_validacion = sum(
            (
                pago.monto
                for pago in pagos_cotizacion
                if pago.estado_pago == "Pendiente"
            ),
            Decimal("0.00")
        )

        saldo_pendiente = max(
            Decimal("0.00"),
            cotizacion.total - total_aprobado
        )

        monto_disponible_registrar = max(
            Decimal("0.00"),
            cotizacion.total - total_registrado
        )

        datos_cotizaciones.append({
            "cotizacion": cotizacion,
            "categoria": categoria,
            "total_aprobado": total_aprobado,
            "total_pendiente_validacion": total_pendiente_validacion,
            "saldo_pendiente": saldo_pendiente,
            "monto_disponible_registrar": monto_disponible_registrar,
        })

    return render(
        request,
        "registrar_pago.html",
        {
            "datos_cotizaciones": datos_cotizaciones,
            "metodos_pago": metodos_pago,
        }
    )





@login_required(login_url="/login/")
@require_POST
def registrar_pago(request):
    ruta = None
    ruta_dte = None

    try:
        cotizacion_id = request.POST.get("cotizacion_id", "").strip()
        metodo_pago_id = request.POST.get("metodo_pago_id", "").strip()
        tipo_pago = request.POST.get("tipo_pago", "Anticipo").strip()
        comprobante = request.FILES.get("comprobante")
        numero_dte = request.POST.get("numero_dte", "").strip()
        archivo_dte = request.FILES.get("archivo_dte")
        if numero_dte and not archivo_dte:
            return JsonResponse({
                "ok": False,
                "error": "Adjunta el archivo correspondiente al DTE."
            }, status=400)

        if archivo_dte and not numero_dte:
            return JsonResponse({
                "ok": False,
                "error": "Ingresa el número del DTE."
            }, status=400)

        if archivo_dte:
            nombre_dte = archivo_dte.name.lower()
            extensiones_permitidas = (".pdf", ".jpg", ".jpeg", ".png")

            if not nombre_dte.endswith(extensiones_permitidas):
                return JsonResponse({
                    "ok": False,
                    "error": "El DTE debe ser PDF, JPG, JPEG o PNG."
                }, status=400)

            if archivo_dte.size <= 0 or archivo_dte.size > 5 * 1024 * 1024:
                return JsonResponse({
                    "ok": False,
                    "error": "El archivo DTE debe pesar entre 1 byte y 5 MB."
                }, status=400)

            inicio_dte = archivo_dte.read(8)
            archivo_dte.seek(0)

            es_pdf_dte = inicio_dte.startswith(b"%PDF-")
            es_jpeg_dte = inicio_dte.startswith(b"\xff\xd8\xff")
            es_png_dte = inicio_dte.startswith(b"\x89PNG\r\n\x1a\n")

            if not (es_pdf_dte or es_jpeg_dte or es_png_dte):
                return JsonResponse({
                    "ok": False,
                    "error": "El contenido del DTE no corresponde a un PDF o imagen válida."
                }, status=400)

        try:
            monto = Decimal(request.POST.get("monto", "0"))
        except (InvalidOperation, ValueError):
            return JsonResponse({
                "ok": False,
                "error": "El monto ingresado no es válido."
            }, status=400)

        if not cotizacion_id or not metodo_pago_id:
            return JsonResponse({
                "ok": False,
                "error": "Selecciona una cotización y un método de pago."
            }, status=400)

        if not monto.is_finite() or monto <= 0:
            return JsonResponse({
                "ok": False,
                "error": "El monto debe ser mayor que cero."
            }, status=400)

        if tipo_pago not in ("Anticipo", "Abono", "Pago final"):
            return JsonResponse({
                "ok": False,
                "error": "El tipo de pago no es válido."
            }, status=400)

        if not comprobante:
            return JsonResponse({
                "ok": False,
                "error": "Adjunta el comprobante del pago."
            }, status=400)

        nombre = comprobante.name.lower()
        extensiones_permitidas = (".pdf", ".jpg", ".jpeg", ".png")

        if not nombre.endswith(extensiones_permitidas):
            return JsonResponse({
                "ok": False,
                "error": "Solo se permiten archivos PDF, JPG, JPEG o PNG."
            }, status=400)

        if comprobante.size <= 0 or comprobante.size > 5 * 1024 * 1024:
            return JsonResponse({
                "ok": False,
                "error": "El archivo debe pesar entre 1 byte y 5 MB."
            }, status=400)

        # Verificar firmas básicas del contenido del archivo.
        inicio = comprobante.read(8)
        comprobante.seek(0)

        es_pdf = inicio.startswith(b"%PDF-")
        es_jpeg = inicio.startswith(b"\xff\xd8\xff")
        es_png = inicio.startswith(b"\x89PNG\r\n\x1a\n")

        if not (es_pdf or es_jpeg or es_png):
            return JsonResponse({
                "ok": False,
                "error": "El contenido del archivo no corresponde a un PDF o imagen admitida."
            }, status=400)

        with transaction.atomic():
            cotizacion = Cotizaciones.objects.select_for_update().get(
                cotizacion_id=cotizacion_id
            )

            if cotizacion.estado != "Aceptada":
                return JsonResponse({
                    "ok": False,
                    "error": "La cotización debe estar aceptada antes de registrar el pago."
                }, status=400)

            metodo_pago = MetodosPago.objects.get(
                metodo_pago_id=metodo_pago_id,
                estado=True
            )

            anticipo_requerido = (
                cotizacion.total * Decimal("0.50")
            ).quantize(Decimal("0.01"))

            # Los pagos pendientes también se consideran para evitar
            # registrar varias solicitudes que excedan el total.
            pagos_existentes = Pagos.objects.filter(
                cotizacion=cotizacion
            ).exclude(estado_pago="Rechazado")

            total_registrado = sum(
                (p.monto for p in pagos_existentes),
                Decimal("0.00")
            )

            if total_registrado + monto > cotizacion.total:
                return JsonResponse({
                    "ok": False,
                    "error": "El pago supera el saldo disponible de la cotización."
                }, status=400)

            evento = cotizacion.evento

            # Se conserva evento_id cuando la cotización corresponde
            # a un evento; en hospedaje puede ser nulo.
            ruta = default_storage.save(
                f"comprobantes/{uuid.uuid4().hex}{nombre[-5:] if nombre.endswith('.jpeg') else nombre[-4:]}",
                ContentFile(comprobante.read())
            )
            if archivo_dte:
                extension_dte = os.path.splitext(archivo_dte.name)[1].lower()

                ruta_dte = default_storage.save(
                    f"dtes/{uuid.uuid4().hex}{extension_dte}",
                    ContentFile(archivo_dte.read())
                )

            Pagos.objects.create(
                evento=evento,
                cotizacion=cotizacion,
                metodo_pago=metodo_pago,
                fecha_pago=timezone.localdate(),
                monto=monto,
                tipo_pago=tipo_pago,
                estado_pago="Pendiente",
                comprobante_url=ruta,
                numero_dte=numero_dte or None,
                archivo_dte=ruta_dte,
                fecha_registro=timezone.now(),
                observaciones="Pendiente de validación del personal."
            )

        return JsonResponse({
            "ok": True,
            "mensaje": "Pago registrado correctamente. Está pendiente de validación.",
            "anticipo_requerido": str(anticipo_requerido),
            "pendiente_validacion": True
        })

    except (
        Cotizaciones.DoesNotExist,
        MetodosPago.DoesNotExist,
        ValueError,
        InvalidOperation,
    ):
        if ruta:
            default_storage.delete(ruta)

       
        return JsonResponse({
            "ok": False,
            "error": "La cotización, el método de pago o los datos proporcionados no son válidos."
        }, status=400)

    except Exception:
        if ruta:
            default_storage.delete(ruta)

        if ruta_dte:
            default_storage.delete(ruta_dte)


        import logging
        logging.exception("Error al registrar el pago")

        return JsonResponse({
            "ok": False,
            "error": "Ocurrió un error al registrar el pago. Revisa los registros del servidor."
        }, status=500)



@login_required(login_url="/login/")
def lista_cotizaciones(request):
    cotizaciones = Cotizaciones.objects.all().order_by("-fecha_creacion")

    categoria = request.GET.get("categoria", "")
    estado = request.GET.get("estado", "")
    buscar = request.GET.get("buscar", "").strip()

    if estado in (
        "Borrador", "Enviada", "Aceptada",
        "Rechazada", "Vencida", "Cancelada"
    ):
        cotizaciones = cotizaciones.filter(estado=estado)

    datos = []

    for cotizacion in cotizaciones:
        hospedaje = Hospedaje.objects.filter(
            cotizacion_id=cotizacion.cotizacion_id
        ).select_related("cliente").first()

        tipo = "Hospedaje" if hospedaje else "Evento"

        if categoria and categoria != tipo:
            continue

        
        if hospedaje:
            cliente_nombre = (
                hospedaje.cliente.nombre
                if hospedaje.cliente else "Sin cliente"
            )
        else:
            evento = cotizacion.evento if cotizacion.evento_id else None

            cliente_nombre = (
                evento.cliente.nombre
                if evento and evento.cliente
                else "Sin cliente asociado"
            )


        if buscar and (
            buscar.lower() not in cotizacion.numero_cotizacion.lower()
            and buscar.lower() not in cliente_nombre.lower()
        ):
            continue

        datos.append({
            "cotizacion": cotizacion,
            "categoria": tipo,
            "cliente_nombre": cliente_nombre,
        })

    return render(
        request,
        "cotizaciones.html",
        {
            "datos": datos,
            "categoria_seleccionada": categoria,
            "estado_seleccionado": estado,
            "busqueda": buscar,
            "estados": [
                "Borrador", "Enviada", "Aceptada",
                "Rechazada", "Vencida", "Cancelada"
            ],
        }
    )


@login_required(login_url="/login/")
@require_POST
def actualizar_estado_cotizacion(request, cotizacion_id):
    estado_nuevo = request.POST.get("estado", "").strip()

    estados_permitidos = {
        "Borrador", "Enviada", "Aceptada",
        "Rechazada", "Vencida", "Cancelada"
    }

    if estado_nuevo not in estados_permitidos:
        return JsonResponse({
            "ok": False,
            "error": "El estado seleccionado no es válido."
        }, status=400)

    cotizacion = get_object_or_404(
        Cotizaciones,
        cotizacion_id=cotizacion_id
    )

    cotizacion.estado = estado_nuevo
    cotizacion.save(update_fields=["estado"])

    return redirect("lista_cotizaciones")


@login_required(login_url="/login/")
def detalle_cotizacion(request, cotizacion_id):
    cotizacion = get_object_or_404(
        Cotizaciones,
        cotizacion_id=cotizacion_id
    )

    hospedaje = Hospedaje.objects.filter(
        cotizacion_id=cotizacion.cotizacion_id
    ).select_related("cliente").first()

    evento = cotizacion.evento if cotizacion.evento_id else None

    detalles = DetalleCotizacion.objects.filter(
        cotizacion=cotizacion
    )

    habitaciones = []

    if hospedaje:
        habitaciones = DetalleHospedaje.objects.filter(
            id_hospedaje=hospedaje
        ).select_related(
            "id_habitaciones",
            "id_unidad"
        )

    pagos = Pagos.objects.filter(
        cotizacion=cotizacion
    ).select_related("metodo_pago").order_by("-fecha_pago")

    total_pagado = sum(
    (
        pago.monto
        for pago in pagos
        if pago.estado_pago == "Aprobado"
    ),
    Decimal("0.00")
    )

    saldo_pendiente = max(
        cotizacion.total - total_pagado,
        Decimal("0.00")
    )

    return render(
        request,
        "detalle_cotizacion.html",
        {
            "cotizacion": cotizacion,
            "hospedaje": hospedaje,
            "evento": evento,
            "detalles": detalles,
            "habitaciones": habitaciones,
            "pagos": pagos,
            "total_pagado": total_pagado,
            "saldo_pendiente": saldo_pendiente,
            "cliente": (
                hospedaje.cliente
                if hospedaje
                else evento.cliente if evento else None
            ),
        }
    )




def pdf_cotizacion(request, cotizacion_id):
    from io import BytesIO
    import os
    from decimal import Decimal

    from django.conf import settings
    from django.http import HttpResponse
    from django.shortcuts import get_object_or_404
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer,
        Table,
        TableStyle,
        Image,
    )
    from xml.sax.saxutils import escape

    cotizacion = get_object_or_404(
        Cotizaciones.objects.select_related(
            "evento__cliente",
            "evento__tipo_evento",
            "evento__area",
        ),
        cotizacion_id=cotizacion_id,
    )

    evento = cotizacion.evento

    if not evento:
        return HttpResponse(
            "La cotización no tiene un evento asociado.",
            status=400,
        )

    cliente = evento.cliente

    detalles = list(
        DetalleCotizacion.objects.filter(
            cotizacion=cotizacion
        ).order_by("detalle_cotizacion_id")
    )

    # Restricciones activas que se imprimen en todas las cotizaciones.
    restricciones = RestriccionesCotizacion.objects.filter(
        estado=True
    ).order_by("orden", "id_restriccion")

    # Recuperar paquete y modalidad elegida. Se conserva compatibilidad
    # con cotizaciones anteriores que solo guardaban el nombre del paquete.
    observaciones_cotizacion = cotizacion.observaciones or ""
    paquete_nombre = "Paquete seleccionado"
    subpaquete_nombre = ""
    paquete_meta = {}
    marcador_meta = "[[PAQUETE_META]]"

    if marcador_meta in observaciones_cotizacion:
        try:
            meta_texto = observaciones_cotizacion.split(marcador_meta, 1)[1].strip()
            paquete_meta = json.loads(meta_texto)
        except (json.JSONDecodeError, TypeError):
            paquete_meta = {}

    paquete_nombre = (paquete_meta.get("paquete_nombre") or "").strip()
    subpaquete_nombre = (paquete_meta.get("subpaquete_nombre") or "").strip()

    if not paquete_nombre:
        prefijo = "Paquete seleccionado:"
        if prefijo in observaciones_cotizacion:
            paquete_nombre = (
                observaciones_cotizacion.split(prefijo, 1)[1]
                .split(".", 1)[0]
                .strip()
            ) or paquete_nombre

    print("========== DEBUG PAQUETE PDF ==========")
    print("ID guardado:", paquete_meta.get("paquete_id"))
    print("Nombre paquete:", paquete_nombre)
    print("Subpaquete:", subpaquete_nombre)
    print("=====================================")

    paquete_id_guardado = str(paquete_meta.get("paquete_id") or "")
    nombre_paquete_norm = paquete_nombre.lower()
    nombre_modalidad_norm = subpaquete_nombre.lower()

    # =========================================================
    # EVENTO PRIVADO ESTÁNDAR - ID 4
    # Pollo, Carne o Vegetariano: mismos servicios
    # =========================================================
    if paquete_id_guardado == "4":

        lineas_paquete = [
            "Mantelería",
            "Sonido ambiente y micrófono",
            "Aire acondicionado",
            "Servicio de catering",
        ]

    # =========================================================
    # EVENTO PRIVADO PREMIUM - ID 1
    # Pollo, Carne o Vegetariano: mismos servicios
    # =========================================================
    elif paquete_id_guardado == "1":

        lineas_paquete = [
            "Refill de gaseosa",
            "Estación de café",
            "Conjunto de base de plato más copa de vidrio",
            "Mantelería Premium",
            "Servilletas de tela",
            "Florero recipiente",
            "Sonido y luces profesionales",
            "Aire acondicionado",
            "Servicio de meseros exclusivo para el evento",
        ]

    # =========================================================
    # EVENTO CORPORATIVO - ID 2
    # Standard o BERAKÁ
    # =========================================================
    elif paquete_id_guardado == "2":

        lineas_paquete = [
            "Hasta ocho horas de uso del Salón Las Orquídeas",
            "Aire acondicionado",
            "Sonido ambiente y micrófonos",
            "Uso de proyector y pantalla",
            "Servicio de catering",
            "Mesas y sillas para el evento",
            "Mantelería",
            "Se agrega 10% de propina sobre el consumo.",
        ]

    # =========================================================
    # EVENTO POR CONSUMO - ID 3
    # =========================================================
    elif paquete_id_guardado == "3":

        lineas_paquete = [
            "Reserva de un espacio dentro del restaurante",
            "Los alimentos y bebidas se pagan según el consumo realizado.",
        ]

    # =========================================================
    # EVENTO NAVIDEÑO - ID 5
    # Standard o Premium
    # =========================================================
    elif paquete_id_guardado == "5":

        lineas_paquete = [
            "Entrada según las condiciones del paquete seleccionado",
            "Plato fuerte navideño a elegir",
            "Acompañamientos navideños",
        ]

        # NAVIDEÑO PREMIUM
        if "premium" in nombre_modalidad_norm:

            lineas_paquete += [
                "Espacio privado en el Salón Las Orquídeas",
                "Aire acondicionado",
                "Sonido profesional",
                "Base de plato y copa",
                "Mantelería Premium y servilletas de tela",
                "Florero recipiente",
                "Refill de gaseosa y estación de café",
                "Servicio de meseros exclusivo para el evento",
                "Cinco horas de uso del salón",
            ]

        # NAVIDEÑO STANDARD
        else:

            lineas_paquete += [
                "Espacio privado en el Salón Las Orquídeas",
                "Aire acondicionado",
                "Sonido profesional",
                "Mantelería",
                "Servicio de meseros exclusivo para el evento",
                "Cinco horas de uso del salón",
            ]

        lineas_paquete.append("Se agrega 10% de propina.")

    # =========================================================
    # EVENTO DE TÉ - ID 6
    # AM o PM
    # =========================================================
    elif paquete_id_guardado == "6":

        lineas_paquete = [
            "Tres horas de uso del Salón Las Orquídeas",
            "Aire acondicionado",
            "Mesas y sillas para el evento",
            "Servicio de catering",
            "Sonido ambiente y micrófono",
            "Mantelería y floreros",
            "Se agrega 10% de propina sobre el consumo.",
        ]

    # =========================================================
    # PAQUETE NO IDENTIFICADO
    # =========================================================
    else:

        lineas_paquete = []

    # =========================================================
    # CONVERTIR EL LISTADO A TEXTO PARA EL PDF
    # =========================================================
    if lineas_paquete:

        detalle_paquete = "<br/>".join(lineas_paquete)

    else:

        detalle_paquete = (
            "Paquete contratado conforme a la modalidad seleccionada. "
            "Los servicios adicionales se detallan por separado."
        )


    # Pagos relacionados con esta cotización.
    pagos = list(
        Pagos.objects.filter(
            cotizacion=cotizacion
        ).select_related(
            "metodo_pago"
        ).order_by(
            "fecha_pago",
            "pago_id",
        )
    )

    cero = Decimal("0.00")

    pagos_aprobados = [
        pago for pago in pagos
        if (pago.estado_pago or "").strip().lower() == "aprobado"
    ]

    pagos_pendientes = [
        pago for pago in pagos
        if (pago.estado_pago or "").strip().lower() == "pendiente"
    ]

    pagos_rechazados = [
        pago for pago in pagos
        if (pago.estado_pago or "").strip().lower() == "rechazado"
    ]

    total_pagado = sum(
        (pago.monto or cero for pago in pagos_aprobados),
        cero,
    )

    total_pendiente_validacion = sum(
        (pago.monto or cero for pago in pagos_pendientes),
        cero,
    )

    total_cotizacion = Decimal(str(cotizacion.total or cero))
    saldo_pendiente = max(cero, total_cotizacion - total_pagado)

    if saldo_pendiente <= cero:
        estado_financiero = "PAGADO COMPLETAMENTE"
    elif total_pagado > cero:
        estado_financiero = "PAGO PARCIAL"
    else:
        estado_financiero = "PENDIENTE DE PAGO"

    # Colores sobrios.
    verde = colors.HexColor("#294C36")
    negro = colors.HexColor("#20231F")
    gris = colors.HexColor("#666A64")
    gris_claro = colors.HexColor("#F3F4F0")
    borde = colors.HexColor("#D9DDD6")
    blanco = colors.white

    buffer = BytesIO()

    documento = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=1.65 * cm,
        leftMargin=1.65 * cm,
        topMargin=1.25 * cm,
        bottomMargin=1.4 * cm,
        title=f"Cotización {cotizacion.numero_cotizacion}",
        author="BERAKÁ Hotel & Restaurante",
    )

    estilos = getSampleStyleSheet()

    estilos.add(ParagraphStyle(
        name="ReporteTitulo",
        parent=estilos["Normal"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=25,
        textColor=verde,
    ))

    estilos.add(ParagraphStyle(
        name="ReporteSubtitulo",
        parent=estilos["Normal"],
        fontSize=8,
        leading=11,
        textColor=gris,
    ))

    estilos.add(ParagraphStyle(
        name="ReporteSeccion",
        parent=estilos["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=verde,
        spaceBefore=12,
        spaceAfter=6,
    ))

    estilos.add(ParagraphStyle(
        name="ReporteTexto",
        parent=estilos["Normal"],
        fontSize=8.5,
        leading=12,
        textColor=negro,
        wordWrap="CJK",
    ))

    estilos.add(ParagraphStyle(
        name="ReportePequeno",
        parent=estilos["Normal"],
        fontSize=7.5,
        leading=10,
        textColor=gris,
    ))

    estilos.add(ParagraphStyle(
        name="ReporteTotal",
        parent=estilos["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=verde,
    ))

    estilos.add(ParagraphStyle(
        name="ReporteDerecha",
        parent=estilos["ReporteTexto"],
        alignment=TA_RIGHT,
    ))

    def texto(valor):
        return escape(str(valor or "No especificado"))

    def dinero(valor):
        return f"${Decimal(str(valor or cero)):,.2f}"

    def fecha(valor):
        return valor.strftime("%d/%m/%Y") if valor else "No especificada"

    def hora(valor):
        return valor.strftime("%I:%M %p") if valor else "No especificada"

    contenido = []

    # Encabezado con logo a la izquierda.
    logo_path = os.path.join(
        settings.BASE_DIR,
        "static",
        "img",
        "logo_beraka.png",
    )

    marca = []

    if os.path.exists(logo_path):
        logo = Image(logo_path, width=2.2 * cm, height=2.2 * cm)
        logo.hAlign = "LEFT"
        marca.append(logo)

    
    marca.extend([
        Paragraph("BERAKÁ", estilos["ReporteTitulo"]),
        Paragraph(
            "HOTEL &amp; RESTAURANTE",
            estilos["ReporteSubtitulo"],
        ),
        Paragraph(
            'Lotificación Germania, Cantón Shucutitan, '
            'calle principal, polígono "A", lote #9, '
            'Ataco, El Salvador',
            ParagraphStyle(
                "DireccionBeraka",
                parent=estilos["ReporteSubtitulo"],
                fontSize=7,
                leading=9,
                textColor=colors.HexColor("#20231F"),
            ),
        ),
    ])


    datos_reporte = [
        Paragraph(
            "<b>COTIZACIÓN</b>",
            ParagraphStyle(
                "CotizacionDerecha",
                parent=estilos["ReporteTexto"],
                fontName="Helvetica-Bold",
                fontSize=15,
                leading=19,
                alignment=TA_RIGHT,
                textColor=verde,
            ),
        ),
        Paragraph(
            f"N.º {texto(cotizacion.numero_cotizacion)}",
            estilos["ReporteDerecha"],
        ),
        Paragraph(
            f"Emisión: {fecha(cotizacion.fecha)}",
            estilos["ReporteDerecha"],
        ),
    ]

    encabezado = Table(
        [[marca, datos_reporte]],
        colWidths=[8.3 * cm, 8.3 * cm],
    )

    encabezado.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LINEBELOW", (0, 0), (-1, -1), 1.2, verde),
    ]))

    contenido.append(encabezado)
    contenido.append(Spacer(1, 8))

    # Datos del cliente.
    contenido.append(Paragraph("INFORMACIÓN DEL CLIENTE", estilos["ReporteSeccion"]))

    datos_cliente = [
        [
            Paragraph("<b>Cliente</b>", estilos["ReporteTexto"]),
            Paragraph(texto(cliente.nombre), estilos["ReporteTexto"]),
            Paragraph("<b>Teléfono</b>", estilos["ReporteTexto"]),
            Paragraph(texto(cliente.telefono), estilos["ReporteTexto"]),
        ],
        [
            Paragraph("<b>Correo</b>", estilos["ReporteTexto"]),
            Paragraph(texto(cliente.correo), estilos["ReporteTexto"]),
            Paragraph("<b>Invitados</b>", estilos["ReporteTexto"]),
            Paragraph(str(evento.total_invitados or 0), estilos["ReporteTexto"]),
        ],
    ]

    tabla_cliente = Table(
        datos_cliente,
        colWidths=[2.1 * cm, 6.2 * cm, 2.1 * cm, 6.2 * cm],
    )
    tabla_cliente.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (-1, -1), gris_claro),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    contenido.append(tabla_cliente)

    # Datos del evento.
    contenido.append(Paragraph("INFORMACIÓN DEL EVENTO", estilos["ReporteSeccion"]))

    tipo_evento = (
        evento.tipo_evento.nombre
        if evento.tipo_evento else "No especificado"
    )
    area_evento = (
        evento.area.nombre
        if evento.area else "No especificado"
    )

    datos_evento = [
        [
            Paragraph("<b>Tipo</b>", estilos["ReporteTexto"]),
            Paragraph(texto(tipo_evento), estilos["ReporteTexto"]),
            Paragraph("<b>Lugar</b>", estilos["ReporteTexto"]),
            Paragraph(texto(area_evento), estilos["ReporteTexto"]),
        ],
        [
            Paragraph("<b>Fecha</b>", estilos["ReporteTexto"]),
            Paragraph(fecha(evento.fecha_evento), estilos["ReporteTexto"]),
            Paragraph("<b>Horario</b>", estilos["ReporteTexto"]),
            Paragraph(
                f"{hora(evento.hora_inicio)} - {hora(evento.hora_fin)}",
                estilos["ReporteTexto"],
            ),
        ],
    ]

    tabla_evento = Table(
        datos_evento,
        colWidths=[2.1 * cm, 6.2 * cm, 2.1 * cm, 6.2 * cm],
    )
    tabla_evento.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, -1), (-1, -1), 0.5, borde),
    ]))
    contenido.append(tabla_evento)

    # Un único cuadro para el paquete seleccionado.
   
    # Presentar el paquete de forma general, sin detallar artículos.
    contenido.append(
        Paragraph("PAQUETE CONTRATADO", estilos["ReporteSeccion"])
    )

    titulo_modalidad = (
        f"<br/><b>Modalidad: {texto(subpaquete_nombre)}</b>"
        if subpaquete_nombre else ""
    )
    texto_paquete = (
        f"<b>{texto(paquete_nombre)}</b>{titulo_modalidad}<br/><br/>"
        f"{detalle_paquete}"
    )

    tabla_paquete = Table(
        [[Paragraph(texto_paquete, estilos["ReporteTexto"])]],
        colWidths=[16.6 * cm],
    )

    tabla_paquete.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.8, verde),
        ("BACKGROUND", (0, 0), (-1, -1), gris_claro),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))

    contenido.append(tabla_paquete)


    
    # Mostrar únicamente conceptos con importe positivo.
    # Los incluidos en el paquete se guardan con importe cero.
    
# Excluir los conceptos marcados como incluidos.
# Los extras deben identificarse como conceptos adicionales.
    
# No desglosar los platos ni servicios incluidos en el paquete.
# Mostrar únicamente los servicios opcionales cobrados por separado.
    
    # Mostrar todos los conceptos adicionales seleccionados manualmente.
    # Los incluidos en el paquete no se guardan como detalles individuales.
    extras = detalles

    if extras:
        contenido.append(Paragraph("SERVICIOS SELECCIONADOS", estilos["ReporteSeccion"]))

        filas_extras = [[
            Paragraph("<b>Concepto</b>", estilos["ReportePequeno"]),
            Paragraph("<b>Cantidad</b>", estilos["ReportePequeno"]),
            Paragraph("<b>Importe</b>", estilos["ReportePequeno"]),
        ]]

        for detalle in extras:

            cantidad = detalle.cantidad or 0

            # Evitar decimales cuando la cantidad es entera
            if cantidad == int(cantidad):
                cantidad_texto = str(int(cantidad))
            else:
                cantidad_texto = f"{cantidad:g}"

            unidad = (detalle.unidad or "").strip().lower()

            if unidad == "persona":
                unidad_texto = (
                    "persona" if cantidad == 1 else "personas"
                )
            else:
                unidad_texto = unidad

            cantidad_final = (
                f"{cantidad_texto} {unidad_texto}"
                if unidad_texto
                else cantidad_texto
            )

            filas_extras.append([
                Paragraph(
                    texto(detalle.concepto),
                    estilos["ReporteTexto"],
                ),
                Paragraph(
                    cantidad_final,
                    estilos["ReporteTexto"],
                ),
                Paragraph(
                    dinero(detalle.subtotal),
                    estilos["ReporteDerecha"],
                ),
            ])

        tabla_extras = Table(
            filas_extras,
            colWidths=[10.0 * cm, 3.2 * cm, 3.4 * cm],
            repeatRows=1,
        )

        tabla_extras.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), gris_claro),
            ("TEXTCOLOR", (0, 0), (-1, -1), negro),
            ("LINEBELOW", (0, 0), (-1, 0), 0.8, verde),
            ("LINEBELOW", (0, 1), (-1, -1), 0.3, borde),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))

        contenido.append(tabla_extras)

    # Resumen económico.
    contenido.append(Paragraph("RESUMEN ECONÓMICO", estilos["ReporteSeccion"]))

    filas_resumen = [
        ["Subtotal", dinero(cotizacion.subtotal)],
        ["Descuento", f"-{dinero(cotizacion.descuento)}"],
        [
            f"Propina ({cotizacion.porcentaje_propina or 0}%)",
            dinero(cotizacion.monto_propina),
        ],
        ["TOTAL DE LA COTIZACIÓN", dinero(total_cotizacion)],
    ]

    tabla_resumen = Table(
        [
            [
                Paragraph(
                    f"<b>{texto(etiqueta)}</b>" if indice == 3 else texto(etiqueta),
                    estilos["ReporteTexto"],
                ),
                Paragraph(
                    f"<b>{importe}</b>" if indice == 3 else importe,
                    estilos["ReporteDerecha"],
                ),
            ]
            for indice, (etiqueta, importe) in enumerate(filas_resumen)
        ],
        colWidths=[10.5 * cm, 6.1 * cm],
        hAlign="RIGHT",
    )
    tabla_resumen.setStyle(TableStyle([
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("LINEABOVE", (0, 3), (-1, 3), 1, verde),
        ("BACKGROUND", (0, 3), (-1, 3), gris_claro),
        ("TEXTCOLOR", (0, 3), (-1, 3), verde),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    contenido.append(tabla_resumen)

    # Estado financiero y saldo.
    contenido.append(Paragraph("REPORTE DE PAGOS", estilos["ReporteSeccion"]))

    resumen_pagos = [
        [
            Paragraph("<b>Total de la cotización</b>", estilos["ReporteTexto"]),
            Paragraph(dinero(total_cotizacion), estilos["ReporteDerecha"]),
        ],
        [
            Paragraph("<b>Total pagado y aprobado</b>", estilos["ReporteTexto"]),
            Paragraph(dinero(total_pagado), estilos["ReporteDerecha"]),
        ],
        [
            Paragraph("<b>Pagos pendientes de validación</b>", estilos["ReporteTexto"]),
            Paragraph(dinero(total_pendiente_validacion), estilos["ReporteDerecha"]),
        ],
        [
            Paragraph("<b>Saldo pendiente de pago</b>", estilos["ReporteTexto"]),
            Paragraph(
                f"<b>{dinero(saldo_pendiente)}</b>",
                estilos["ReporteDerecha"],
            ),
        ],
        [
            Paragraph("<b>Estado financiero</b>", estilos["ReporteTexto"]),
            Paragraph(f"<b>{estado_financiero}</b>", estilos["ReporteDerecha"]),
        ],
    ]

    tabla_pagos_resumen = Table(
        resumen_pagos,
        colWidths=[10.5 * cm, 6.1 * cm],
    )
    tabla_pagos_resumen.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.6, borde),
        ("LINEBELOW", (0, 0), (-1, -2), 0.3, borde),
        ("BACKGROUND", (0, 3), (-1, 4), gris_claro),
        ("TEXTCOLOR", (0, 4), (-1, 4), verde),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    contenido.append(tabla_pagos_resumen)

    # Historial de pagos, incluyendo pendientes y rechazados.
    contenido.append(Paragraph("DETALLE DEL HISTORIAL DE PAGOS", estilos["ReporteSeccion"]))

    if pagos:
        filas_historial = [[
            Paragraph("<b>Fecha</b>", estilos["ReportePequeno"]),
            Paragraph("<b>Tipo</b>", estilos["ReportePequeno"]),
            Paragraph("<b>Método</b>", estilos["ReportePequeno"]),
            Paragraph("<b>Monto</b>", estilos["ReportePequeno"]),
            Paragraph("<b>Estado</b>", estilos["ReportePequeno"]),
            Paragraph("<b>N.º de DTE</b>", estilos["ReportePequeno"]),
        ]]

        for pago in pagos:
            metodo = (
                pago.metodo_pago.nombre
                if pago.metodo_pago else "No especificado"
            )

            filas_historial.append([
                Paragraph(fecha(pago.fecha_pago), estilos["ReportePequeno"]),
                Paragraph(
                    texto(pago.tipo_pago or "No especificado"),
                    estilos["ReportePequeno"],
                ),
                Paragraph(
                    texto(metodo),
                    estilos["ReportePequeno"],
                ),
                Paragraph(
                    dinero(pago.monto),
                    estilos["ReporteDerecha"],
                ),
                Paragraph(
                    texto(pago.estado_pago or "Pendiente"),
                    estilos["ReportePequeno"],
                ),
                Paragraph(
                    texto(pago.numero_dte or "Sin DTE"),
                    estilos["ReportePequeno"],
                ),
            ])

        tabla_historial = Table(
            filas_historial,
            colWidths=[2.0 * cm, 2.0 * cm, 3.4 * cm, 2.5 * cm, 3.0 * cm, 3.7 * cm],
            repeatRows=1,
        )
        tabla_historial.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), gris_claro),
            ("LINEBELOW", (0, 0), (-1, 0), 0.8, verde),
            ("LINEBELOW", (0, 1), (-1, -1), 0.3, borde),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        contenido.append(tabla_historial)
    else:
        contenido.append(Paragraph(
            "No hay pagos registrados para esta cotización.",
            estilos["ReporteTexto"],
        ))

    if pagos_rechazados:
        contenido.append(Spacer(1, 4))
        contenido.append(Paragraph(
            f"Nota: hay {len(pagos_rechazados)} pago(s) rechazado(s). "
            "No se incluyen en el total pagado.",
            estilos["ReportePequeno"],
        ))

    # Observaciones del evento.
    if evento.observaciones:
        contenido.append(Paragraph("OBSERVACIONES DEL EVENTO", estilos["ReporteSeccion"]))
        contenido.append(Paragraph(texto(evento.observaciones), estilos["ReporteTexto"]))
        # Restricciones y condiciones del evento.

    contenido.append(Spacer(1, 14))
    contenido.append(Paragraph(
        "Gracias por considerar a BERAKÁ para su evento.",
        ParagraphStyle(
            "ReporteCierre",
            parent=estilos["Normal"],
            alignment=TA_CENTER,
            textColor=verde,
            fontName="Helvetica-Bold",
            fontSize=9,
        ),
    ))
    contenido.append(Spacer(1, 3))
    contenido.append(Paragraph(
        "Reporte generado por el sistema de cotizaciones de BERAKÁ.",
        ParagraphStyle(
            "ReportePie",
            parent=estilos["Normal"],
            alignment=TA_CENTER,
            textColor=gris,
            fontSize=7,
        ),
    ))
        # Restricciones y condiciones del evento.
    restricciones = RestriccionesCotizacion.objects.filter(
        estado=True
    ).order_by("orden")

    if restricciones.exists():
        contenido.append(Spacer(1, 15))

        contenido.append(
            Paragraph(
                "RESTRICCIONES Y CONDICIONES DEL EVENTO",
                estilos["ReporteSeccion"]
            )
        )

        for restriccion in restricciones:
            contenido.append(
                Paragraph(
                    f"<b>{texto(restriccion.titulo)}:</b> "
                    f"{texto(restriccion.descripcion)}",
                    estilos["ReporteTexto"]
                )
            )
            contenido.append(Spacer(1, 5))

    documento.build(contenido)

    pdf = buffer.getvalue()
    buffer.close()

    respuesta = HttpResponse(pdf, content_type="application/pdf")
    respuesta["Content-Disposition"] = (
        f'attachment; filename="Cotizacion_{cotizacion.numero_cotizacion}.pdf"'
    )
    return respuesta


@login_required(login_url="/login/")
def pagos_cotizacion_json(request, cotizacion_id):
    if not request.user.has_perm("eventos.validar_pagos"):
        return JsonResponse(
            {"ok": False, "error": "No tienes permiso para validar pagos."},
            status=403
        )

    try:
        cotizacion = Cotizaciones.objects.get(
            cotizacion_id=cotizacion_id
        )
        # Comisión por cancelación
        comision_cancelacion = Decimal("0.00")

        if (cotizacion.estado or "").strip().lower() == "cancelada":
            base_sin_propina = (
                Decimal(str(cotizacion.total or 0))
                - Decimal(str(cotizacion.monto_propina or 0))
            )

            comision_cancelacion = (
                base_sin_propina * Decimal("0.05")
            ).quantize(
                Decimal("0.01"),
                rounding=ROUND_DOWN
            )

        pagos = Pagos.objects.filter(
            cotizacion=cotizacion
        ).select_related("metodo_pago").order_by("-fecha_registro")

        datos_pagos = []

        for pago in pagos:
            datos_pagos.append({
                "pago_id": pago.pago_id,
                "monto": str(pago.monto),
                "fecha_pago": pago.fecha_pago.strftime("%d/%m/%Y"),
                "metodo_pago": (
                    pago.metodo_pago.nombre
                    if pago.metodo_pago else "No especificado"
                ),
                "tipo_pago": pago.tipo_pago or "No especificado",
                "estado_pago": pago.estado_pago or "Pendiente",
                "observaciones": pago.observaciones or "",
                "comprobante_url": (
                    request.build_absolute_uri(
                        default_storage.url(pago.comprobante_url)
                    )
                    if pago.comprobante_url else None
                ),
                "numero_dte": pago.numero_dte or "",
                "archivo_dte_url": (
                    request.build_absolute_uri(
                        default_storage.url(pago.archivo_dte)
                    )
                    if pago.archivo_dte else None
                ),
            })

            # Comisión del 5% únicamente para cotizaciones canceladas
            # Inicializar comisión en cero para todas las cotizaciones
            comision_cancelacion = Decimal("0.00")

            # Calcular únicamente si está cancelada
            if (cotizacion.estado or "").strip().lower() == "cancelada":

                base_sin_propina = (
                    Decimal(str(cotizacion.total or 0))
                    - Decimal(str(cotizacion.monto_propina or 0))
                )

                comision_cancelacion = (
                    base_sin_propina * Decimal("0.05")
                ).quantize(
                    Decimal("0.01"),
                    rounding=ROUND_DOWN
                )
        return JsonResponse({
        "ok": True,
        "cotizacion": cotizacion.numero_cotizacion,
        "estado": cotizacion.estado,
        "comision_cancelacion": str(comision_cancelacion),
        "pagos": datos_pagos,
    })

    except Cotizaciones.DoesNotExist:

        return JsonResponse(
            {"ok": False, "error": "La cotización no existe."},
            status=404
        )

@login_required(login_url="/login/")
@require_POST
def validar_pago(request, pago_id):
    if not request.user.has_perm("eventos.validar_pagos"):
        return JsonResponse({
            "ok": False,
            "error": "No tienes permiso para validar pagos."
        }, status=403)

    decision = request.POST.get("decision", "").strip()
    observacion = request.POST.get("observacion", "").strip()

    if decision not in ("Aprobado", "Rechazado"):
        return JsonResponse({
            "ok": False,
            "error": "La decisión no es válida."
        }, status=400)

    if decision == "Rechazado" and not observacion:
        return JsonResponse({
            "ok": False,
            "error": "Debes indicar el motivo del rechazo."
        }, status=400)

    try:
        with transaction.atomic():
            pago = Pagos.objects.select_for_update().get(
                pago_id=pago_id
            )

            if pago.estado_pago != "Pendiente":
                return JsonResponse({
                    "ok": False,
                    "error": "Este pago ya fue validado o no está pendiente."
                }, status=400)

            pago.estado_pago = decision
            pago.observaciones = (
                observacion
                if decision == "Rechazado"
                else "Pago aprobado por el personal."
            )
            pago.save(update_fields=[
                "estado_pago",
                "observaciones"
            ])

        return JsonResponse({
            "ok": True,
            "mensaje": (
                "Pago aprobado correctamente."
                if decision == "Aprobado"
                else "Pago rechazado correctamente."
            ),
            "estado_pago": decision
        })

    except Pagos.DoesNotExist:
        return JsonResponse({
            "ok": False,
            "error": "No se encontró el pago."
        }, status=404)

    
@login_required(login_url="/login/")
@require_POST
def subir_dte_pago(request, pago_id):
    if not request.user.has_perm("eventos.validar_pagos"):
        return JsonResponse({
            "ok": False,
            "error": "No tienes permiso para subir DTE."
        }, status=403)

    numero_dte = request.POST.get("numero_dte", "").strip()
    archivo_dte = request.FILES.get("archivo_dte")

    if not numero_dte:
        return JsonResponse({
            "ok": False,
            "error": "Ingresa el número del DTE."
        }, status=400)

    if not archivo_dte:
        return JsonResponse({
            "ok": False,
            "error": "Selecciona el archivo del DTE."
        }, status=400)

    nombre = archivo_dte.name.lower()
    extensiones = (".pdf", ".jpg", ".jpeg", ".png")

    if not nombre.endswith(extensiones):
        return JsonResponse({
            "ok": False,
            "error": "El DTE debe ser PDF, JPG, JPEG o PNG."
        }, status=400)

    if archivo_dte.size <= 0 or archivo_dte.size > 5 * 1024 * 1024:
        return JsonResponse({
            "ok": False,
            "error": "El archivo debe pesar entre 1 byte y 5 MB."
        }, status=400)

    inicio = archivo_dte.read(8)
    archivo_dte.seek(0)

    valido = (
        inicio.startswith(b"%PDF-")
        or inicio.startswith(b"\xff\xd8\xff")
        or inicio.startswith(b"\x89PNG\r\n\x1a\n")
    )

    if not valido:
        return JsonResponse({
            "ok": False,
            "error": "El contenido no corresponde a un PDF o imagen válida."
        }, status=400)

    try:
        pago = Pagos.objects.get(pago_id=pago_id)
    except Pagos.DoesNotExist:
        return JsonResponse({
            "ok": False,
            "error": "No se encontró el pago."
        }, status=404)

    extension = os.path.splitext(nombre)[1]
    ruta_nueva = default_storage.save(
        f"dtes/{uuid.uuid4().hex}{extension}",
        ContentFile(archivo_dte.read())
    )

    ruta_anterior = pago.archivo_dte

    try:
        pago.numero_dte = numero_dte
        pago.archivo_dte = ruta_nueva
        pago.save(update_fields=["numero_dte", "archivo_dte"])
    except Exception:
        default_storage.delete(ruta_nueva)
        raise

    if ruta_anterior and ruta_anterior != ruta_nueva:
        default_storage.delete(ruta_anterior)

    return JsonResponse({
        "ok": True,
        "mensaje": "DTE guardado correctamente."
    })



# ============================================================
# RESERVAS WEB
# ============================================================

@login_required(login_url="login")
def reservas_web(request):
    reservas = ReservaHabitacionWeb.objects.all().order_by("-creado")

    pendientes = reservas.filter(estado="Pendiente").count()

    return render(request, "reservas_web.html", {
        "reservas": reservas,
        "pendientes": pendientes,
    })


@login_required(login_url="login")
def detalle_reserva_web(request, reserva_id):
    reserva = get_object_or_404(
        ReservaHabitacionWeb,
        pk=reserva_id
    )

    # Identificar el tipo solicitado.
    tipo = (
        reserva.tipo_habitacion
        .lower()
        .replace("habitación", "")
        .replace("habitacion", "")
        .strip()
    )

    unidades = HabitacionesUnidades.objects.filter(
        activa=True,
        id_habitaciones__nombre__icontains=tipo,
    ).select_related("id_habitaciones")

    # Solo mostrar unidades disponibles para las fechas solicitadas.
    ocupadas = DetalleHospedaje.objects.filter(
        fecha_check_in__lt=reserva.fecha_salida,
        fecha_check_out__gt=reserva.fecha_entrada,
        id_hospedaje__cotizacion__estado="Aceptada",
    ).values_list("id_unidad_id", flat=True)

    unidades = unidades.exclude(id_unidad__in=ocupadas).filter(
    Q(id_habitaciones__capacidad__gte=reserva.personas)
    | Q(id_habitaciones__capacidad__isnull=True)
)

    if request.method == "POST":
        if reserva.estado != "Pendiente":
            messages.error(request, "Esta solicitud ya fue procesada.")
            return redirect("reservas_web")

        unidad_id = request.POST.get("unidad")

        if not unidad_id:
            messages.error(request, "Selecciona una unidad disponible.")
            return redirect("detalle_reserva_web", reserva_id=reserva.pk)

        try:
            with transaction.atomic():
                # Bloquear solicitud y unidad durante la aprobación.
                reserva = ReservaHabitacionWeb.objects.select_for_update().get(
                    pk=reserva.pk
                )

                if reserva.estado != "Pendiente":
                    messages.error(
                        request,
                        "Esta solicitud ya fue procesada."
                    )
                    return redirect("reservas_web")

                unidad = HabitacionesUnidades.objects.select_for_update().select_related(
                    "id_habitaciones"
                ).get(
                    id_unidad=unidad_id,
                    activa=True,
                    id_habitaciones__nombre__icontains=tipo,
                )

                if (
                    unidad.id_habitaciones.capacidad
                    and unidad.id_habitaciones.capacidad < reserva.personas
                ):
                    messages.error(
                        request,
                        "La capacidad de esta habitación es insuficiente."
                    )
                    return redirect(
                        "detalle_reserva_web",
                        reserva_id=reserva.pk
                    )

                # Comprobar nuevamente que la unidad siga disponible.
                ya_ocupada = DetalleHospedaje.objects.filter(
                    id_unidad=unidad,
                    fecha_check_in__lt=reserva.fecha_salida,
                    fecha_check_out__gt=reserva.fecha_entrada,
                    id_hospedaje__cotizacion__estado="Aceptada",
                ).exists()

                if ya_ocupada:
                    messages.error(
                        request,
                        "La habitación ya fue reservada para esas fechas."
                    )
                    return redirect(
                        "detalle_reserva_web",
                        reserva_id=reserva.pk
                    )

                noches = (
                    reserva.fecha_salida - reserva.fecha_entrada
                ).days

                precio = Decimal(
                    str(unidad.id_habitaciones.precio or 0)
                )

                subtotal = precio * noches
                ahora = timezone.now()

                cliente = Clientes.objects.create(
                    nombre=reserva.nombre,
                    telefono=reserva.telefono,
                    correo=None,
                    fecha_registro=ahora,
                )

                numero = (
                    f"HOS-{ahora:%Y%m%d}-"
                    f"{uuid.uuid4().hex[:8].upper()}"
                )

                cotizacion = Cotizaciones.objects.create(
                    evento=None,
                    numero_cotizacion=numero,
                    fecha=ahora.date(),
                    subtotal=subtotal,
                    porcentaje_propina=Decimal("0.00"),
                    monto_propina=Decimal("0.00"),
                    descuento=Decimal("0.00"),
                    total=subtotal,
                    estado="Aceptada",
                    observaciones=(
                        f"Reserva recibida desde el sitio web. "
                        f"Solicitud #{reserva.pk}. "
                        f"Entrada: {reserva.fecha_entrada}; "
                        f"salida: {reserva.fecha_salida}; "
                        f"personas: {reserva.personas}."
                    ),
                    fecha_creacion=ahora,
                )

                hospedaje = Hospedaje.objects.create(
                    total=subtotal,
                    fecha=ahora,
                    cliente=cliente,
                    cotizacion=cotizacion,
                )

                DetalleHospedaje.objects.create(
                    id_hospedaje=hospedaje,
                    id_habitaciones=unidad.id_habitaciones,
                    id_unidad=unidad,
                    fecha_check_in=reserva.fecha_entrada,
                    fecha_check_out=reserva.fecha_salida,
                    
                )

                reserva.estado = "Aprobada"
                reserva.save(update_fields=["estado"])

            messages.success(
                request,
                f"Reserva aprobada. Cotización: {numero}"
            )
            return redirect("reservas_web")

        except HabitacionesUnidades.DoesNotExist:
            messages.error(
                request,
                "La unidad seleccionada no existe o no corresponde al tipo solicitado."
            )
        except Exception as e:
            messages.error(
                request,
                f"No se pudo aprobar la reserva: {str(e)}"
            )

    return render(request, "detalle_reserva_web.html", {
        "reserva": reserva,
        "unidades": unidades,
    })


@login_required(login_url="login")
@require_POST
def rechazar_reserva_web(request, reserva_id):
    reserva = get_object_or_404(
        ReservaHabitacionWeb,
        pk=reserva_id
    )

    if reserva.estado == "Pendiente":
        reserva.estado = "Rechazada"
        reserva.save(update_fields=["estado"])
        messages.success(request, "La solicitud fue rechazada.")
    else:
        messages.warning(request, "La solicitud ya fue procesada.")

    return redirect("reservas_web")