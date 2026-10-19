import json
import uuid
from datetime import datetime
from decimal import Decimal, InvalidOperation
from django.db.models import Sum, Q
from collections import Counter
from decimal import Decimal, InvalidOperation

from django.shortcuts import render, redirect, get_object_or_404


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

    Cotizaciones, Eventos, Clientes, Pagos

    

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
                incluido = item.get("incluido") is True

                if not nombre or cantidad <= 0 or precio < 0:
                    return JsonResponse({
                        "ok": False,
                        "error": "Hay un concepto con datos inválidos."
                    }, status=400)

                if incluido:
                    importe = Decimal("0.00")
                else:
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


            # Corporativo y consumo llevan 10 % de propina.
            if paquete_id in ("2", "3"):
                porcentaje_propina = Decimal("10.00")
            else:
                porcentaje_propina = Decimal("0.00")

            # Aplicar descuento y calcular propina
            base = max(subtotal - descuento, Decimal("0.00"))

            if paquete_id in ("2", "3"):
                monto_propina = (
                    base * porcentaje_propina / Decimal("100")
                ).quantize(Decimal("0.01"))
            else:
                porcentaje_propina = Decimal("0.00")
                monto_propina = Decimal("0.00")

            total = base + monto_propina            # Guardar todo dentro de una transacción

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

                    cantidad_ninos=0,
                    
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

                        f"Paquete seleccionado: "

                        f"{data.get('paquete_nombre', '')}. "

                        f"{observaciones}"

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
                estado="Borrador",
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

        datos_cotizaciones.append({
            "cotizacion": cotizacion,
            "categoria": categoria,
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

    try:
        cotizacion_id = request.POST.get("cotizacion_id", "").strip()
        metodo_pago_id = request.POST.get("metodo_pago_id", "").strip()
        tipo_pago = request.POST.get("tipo_pago", "Anticipo").strip()
        comprobante = request.FILES.get("comprobante")

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

            Pagos.objects.create(
                evento=evento,
                cotizacion=cotizacion,
                metodo_pago=metodo_pago,
                fecha_pago=timezone.localdate(),
                monto=monto,
                tipo_pago=tipo_pago,
                estado_pago="Pendiente",
                comprobante_url=ruta,
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
            })

        return JsonResponse({
            "ok": True,
            "cotizacion": cotizacion.numero_cotizacion,
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

    
