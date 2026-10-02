from decimal import Decimal

from django.db import transaction



from eventos.models import (

    TiposEvento,

    ProductosEvento,

    Servicios,

    ElementosMontaje,

    PaquetesEvento,

    PaqueteProductos,

    PaqueteServicios,

    PaqueteMontaje,

)



print("\n==========================================")

print("   CARGANDO PAQUETES BERAKÁ")

print("==========================================\n")





# ============================================================

# FUNCIONES AUXILIARES

# ============================================================



def obtener_tipo(nombre, descripcion):

    tipo, creado = TiposEvento.objects.update_or_create(

        nombre=nombre,

        defaults={

            "descripcion": descripcion,

            "estado": True,

        },

    )



    print(

        f"Tipo de evento: {nombre} "

        f"({'CREADO' if creado else 'ACTUALIZADO'})"

    )



    return tipo





def obtener_producto(nombre):

    producto = ProductosEvento.objects.filter(

        nombre=nombre,

        estado=True

    ).first()



    if not producto:

        raise ValueError(

            f'No se encontró el producto "{nombre}". '

            f'Revisa que exista en ProductosEvento.'

        )



    return producto





def obtener_servicio(nombre):

    servicio = Servicios.objects.filter(

        nombre=nombre,

        estado=True

    ).first()



    if not servicio:

        raise ValueError(

            f'No se encontró el servicio "{nombre}". '

            f'Revisa que exista en Servicios.'

        )



    return servicio





def obtener_montaje(nombre):

    elemento = ElementosMontaje.objects.filter(

        nombre=nombre,

        estado=True

    ).first()



    if not elemento:

        raise ValueError(

            f'No se encontró el elemento de montaje "{nombre}". '

            f'Revisa que exista en ElementosMontaje.'

        )



    return elemento





def crear_paquete(

    nombre,

    descripcion,

    tipo_evento,

    precio_base,

    cantidad_personas_base=1,

):

    paquete, creado = PaquetesEvento.objects.update_or_create(

        nombre=nombre,

        tipo_evento=tipo_evento,

        defaults={

            "descripcion": descripcion,

            "precio_base": Decimal(str(precio_base)),

            "cantidad_personas_base": cantidad_personas_base,

            "activo": True,

        },

    )



    print(

        f"  Paquete: {nombre} "

        f"({'CREADO' if creado else 'ACTUALIZADO'})"

    )



    return paquete





def agregar_producto(paquete, nombre, cantidad=1, obligatorio=True):

    producto = obtener_producto(nombre)



    PaqueteProductos.objects.update_or_create(

        paquete=paquete,

        producto=producto,

        defaults={

            "cantidad": Decimal(str(cantidad)),

            "obligatorio": obligatorio,

        },

    )



    print(f"    + Producto: {nombre}")





def agregar_servicio(paquete, nombre, cantidad=1, obligatorio=True):

    servicio = obtener_servicio(nombre)



    PaqueteServicios.objects.update_or_create(

        paquete=paquete,

        servicio=servicio,

        defaults={

            "cantidad": Decimal(str(cantidad)),

            "obligatorio": obligatorio,

        },

    )



    print(f"    + Servicio: {nombre}")





def agregar_montaje(paquete, nombre, cantidad=1, obligatorio=True):

    elemento = obtener_montaje(nombre)



    PaqueteMontaje.objects.update_or_create(

        paquete=paquete,

        elemento=elemento,

        defaults={

            "cantidad": Decimal(str(cantidad)),

            "obligatorio": obligatorio,

        },

    )



    print(f"    + Montaje: {nombre}")





# ============================================================

# CARGA PRINCIPAL

# ============================================================



with transaction.atomic():



    # ========================================================

    # 1. TIPOS DE EVENTO

    # ========================================================



    tipo_consumo = obtener_tipo(

        "EVENTO POR CONSUMO",

        "Evento realizado dentro del restaurante mediante selección "

        "de productos del menú. Se paga únicamente el consumo."

    )



    tipo_capacitacion = obtener_tipo(

        "CAPACITACIONES",

        "Evento privado para capacitaciones con alimentación "

        "y uso del Salón Las Orquídeas."

    )



    tipo_vip = obtener_tipo(

        "VIP",

        "Experiencia completa para eventos con alimentación, "

        "bebidas, montaje y servicio."

    )



    tipo_infantil = obtener_tipo(

        "CUMPLEAÑOS INFANTIL",

        "Paquete infantil para celebración de cumpleaños."

    )





    # ========================================================

    # 2. EVENTO POR CONSUMO

    # ========================================================



    paquete_consumo = crear_paquete(

        nombre="EVENTO POR CONSUMO",

        descripcion=(

            "El cliente selecciona entrada, plato fuerte, bebida "

            "y postre del menú. Se reserva un espacio dentro "

            "del restaurante sin costo adicional. "

            "Se agrega 10% de propina sobre el consumo."

        ),

        tipo_evento=tipo_consumo,

        precio_base=0,

        cantidad_personas_base=1,

    )



    # IMPORTANTE:

    # Aquí NO agregamos productos específicos.

    # El cliente podrá escogerlos del menú cuando se haga

    # la cotización.





    # ========================================================

    # 3. CAPACITACIONES

    # ========================================================



    paquete_capacitacion = crear_paquete(

        nombre="CAPACITACIONES",

        descripcion=(

            "Incluye entrada, plato fuerte, bebida y postre "

            "seleccionados del menú, más 5 horas de uso del "

            "Salón Las Orquídeas, aire acondicionado, "

            "sonido profesional, proyector, mesas y sillas. "

            "El salón tiene un costo de $250 por 5 horas. "

            "Se agrega 10% de propina sobre el consumo."

        ),

        tipo_evento=tipo_capacitacion,

        precio_base=250,

        cantidad_personas_base=1,

    )



    agregar_servicio(

        paquete_capacitacion,

        "Uso de Salón Las Orquídeas",

        cantidad=1,

        obligatorio=True,

    )





    # ========================================================

    # 4. VIP - VEGETARIANO

    # ========================================================



    paquete_vip_vegetariano = crear_paquete(

        nombre="VIP - VEGETARIANO",

        descripcion=(

            "Paquete VIP con opción vegetariana. "

            "Precio de $33.75 por persona. "

            "Incluye alimentación, bebidas, montaje, "

            "meseros y uso del jardín para ceremonia. "

            "Se agrega 10% de propina."

        ),

        tipo_evento=tipo_vip,

        precio_base=33.75,

        cantidad_personas_base=1,

    )



    agregar_producto(

        paquete_vip_vegetariano,

        "Entrada de ensalada caprese con pesto de la casa",

        1,

        True,

    )



    agregar_producto(

        paquete_vip_vegetariano,

        "Refil de gaseosa",

        1,

        True,

    )



    agregar_producto(

        paquete_vip_vegetariano,

        "Estación de café",

        1,

        True,

    )



    agregar_producto(

        paquete_vip_vegetariano,

        "Descorche de pastel",

        1,

        True,

    )



    agregar_servicio(

        paquete_vip_vegetariano,

        "Uso de jardín para ceremonia",

        1,

        True,

    )



    agregar_servicio(

        paquete_vip_vegetariano,

        "Servicio de sonido y luces",

        1,

        False,

    )



    agregar_servicio(

        paquete_vip_vegetariano,

        "DJ",

        1,

        False,

    )



    agregar_servicio(

        paquete_vip_vegetariano,

        "Barra libre",

        1,

        False,

    )



    agregar_servicio(

        paquete_vip_vegetariano,

        "Descorche de boquitas",

        1,

        False,

    )



    agregar_montaje(

        paquete_vip_vegetariano,

        "Base de plato",

        1,

        True,

    )



    agregar_montaje(

        paquete_vip_vegetariano,

        "Copa",

        1,

        True,

    )



    agregar_montaje(

        paquete_vip_vegetariano,

        "Manteles",

        1,

        True,

    )



    agregar_montaje(

        paquete_vip_vegetariano,

        "Servilleta de tela",

        1,

        True,

    )



    agregar_montaje(

        paquete_vip_vegetariano,

        "Florero",

        1,

        True,

    )





    # ========================================================

    # 5. VIP - POLLO

    # ========================================================



    paquete_vip_pollo = crear_paquete(

        nombre="VIP - POLLO",

        descripcion=(

            "Paquete VIP con opción de pollo. "

            "Precio de $37.25 por persona."

        ),

        tipo_evento=tipo_vip,

        precio_base=37.25,

        cantidad_personas_base=1,

    )



    agregar_producto(

        paquete_vip_pollo,

        "Entrada de ensalada caprese con pesto de la casa",

        1,

        True,

    )



    agregar_producto(

        paquete_vip_pollo,

        "Refil de gaseosa",

        1,

        True,

    )



    agregar_producto(

        paquete_vip_pollo,

        "Estación de café",

        1,

        True,

    )



    agregar_producto(

        paquete_vip_pollo,

        "Descorche de pastel",

        1, 

        True,

    )



    agregar_servicio(

        paquete_vip_pollo,

        "Uso de jardín para ceremonia",

        1,

        True,

    )



    agregar_servicio(

        paquete_vip_pollo,

        "Servicio de sonido y luces",

        1,

        False,

    )



    agregar_servicio(

        paquete_vip_pollo,

        "DJ",

        1,

        False,

    )



    agregar_servicio(

        paquete_vip_pollo,

        "Barra libre",

        1,

        False,

    )



    agregar_servicio(

        paquete_vip_pollo,

        "Descorche de boquitas",

        1,

        False,

    )



    agregar_montaje(

        paquete_vip_pollo,

        "Base de plato",

        1,

        True,

    )



    agregar_montaje(

        paquete_vip_pollo,

        "Copa",

        1,

        True,

    )



    agregar_montaje(

        paquete_vip_pollo,

        "Manteles",

        1,

        True,

    )



    agregar_montaje(

        paquete_vip_pollo,

        "Servilleta de tela",

        1,

        True,

    )



    agregar_montaje(

        paquete_vip_pollo,

        "Florero",

        1,

        True,

    )





    # ========================================================

    # 6. VIP - CARNE

    # ========================================================



    paquete_vip_carne = crear_paquete(

        nombre="VIP - CARNE",

        descripcion=(

            "Paquete VIP con opción de carne. "

            "Precio de $40.75 por persona."

        ),

        tipo_evento=tipo_vip,

        precio_base=40.75,

        cantidad_personas_base=1,

    )



    agregar_producto(

        paquete_vip_carne,

        "Entrada de ensalada caprese con pesto de la casa",

        1,

        True,

    )



    agregar_producto(

        paquete_vip_carne,

        "Refil de gaseosa",

        1,

        True,

    )



    agregar_producto(

        paquete_vip_carne,

        "Estación de café",

        1,

        True,

    )



    agregar_producto(

        paquete_vip_carne,

        "Descorche de pastel",

        1,

        True,

    )



    agregar_servicio(

        paquete_vip_carne,

        "Uso de jardín para ceremonia",

        1,

        True,

    )



    agregar_servicio(

        paquete_vip_carne,

        "Servicio de sonido y luces",

        1,

        False,

    )



    agregar_servicio(

        paquete_vip_carne,

        "DJ",

        1,

        False,

    )



    agregar_servicio(

        paquete_vip_carne,

        "Barra libre",

        1,

        False,

    )



    agregar_servicio(

        paquete_vip_carne,

        "Descorche de boquitas",

        1,

        False,

    )



    agregar_montaje(

        paquete_vip_carne,

        "Base de plato",

        1,

        True,

    )



    agregar_montaje(

        paquete_vip_carne,

        "Copa",

        1,

        True,

    )



    agregar_montaje(

        paquete_vip_carne,

        "Manteles",

        1,

        True,

    )



    agregar_montaje(

        paquete_vip_carne,

        "Servilleta de tela",

        1,

        True,

    )



    agregar_montaje(

        paquete_vip_carne,

        "Florero",

        1,

        True,

    )





    # ========================================================

    # 7. CUMPLEAÑOS INFANTIL

    # ========================================================



    paquete_infantil = crear_paquete(

        nombre="CUMPLEAÑOS INFANTIL",

        descripcion=(

            "Paquete para cumpleaños infantil. "

            "Incluye hamburguesa Jr o nuggets, refill de gaseosa, "

            "estación de café, meseros, descorche de pastel, "

            "manteles y 5 horas de uso del salón por $100 fijo. "

            "Costo por persona indicado en el documento: $14.33."

        ),

        tipo_evento=tipo_infantil,

        precio_base=14.33,

        cantidad_personas_base=1,

    )



    agregar_producto(

        paquete_infantil,

        "Hamburguesa",

        1,

        True,

    )



    agregar_producto(

        paquete_infantil,

        "Refil de gaseosa",

        1,

        True,

    )



    agregar_producto(

        paquete_infantil,

        "Estación de café",

        1,

        True,

    )



    agregar_producto(

        paquete_infantil,

        "Meseros",

        1,

        True,

    )



    agregar_producto(

        paquete_infantil,

        "Descorche de pastel",

        1,

        True,

    )



    agregar_servicio(

    paquete_infantil,

    "Uso de salón infantil",

    1,

    True,

)



    # Para el salón infantil necesitamos el costo fijo

    # de $100 por 5 horas.

    #

    # Si posteriormente quieres manejarlo como servicio

    # independiente en Servicios, se puede agregar.

    #

    # Por ahora se registra dentro de la descripción del paquete.





    print("\n==========================================")

    print("   PAQUETES BERAKÁ CARGADOS CORRECTAMENTE")

    print("==========================================\n")





# ============================================================

# RESUMEN

# ============================================================

print()

print("=" * 60)

print("CATALOGO DE PAQUETES CARGADO CORRECTAMENTE")

print("=" * 60)



print(f"Paquetes creados/actualizados: {PaquetesEvento.objects.count()}")

print(f"Productos de evento: {ProductosEvento.objects.count()}")

print(f"Servicios: {Servicios.objects.count()}")

print(f"Elementos de montaje: {ElementosMontaje.objects.count()}")



print()

print("Paquetes:")

for paquete in PaquetesEvento.objects.all():

    print(f" - {paquete.nombre}")



print()

print("Proceso terminado.")