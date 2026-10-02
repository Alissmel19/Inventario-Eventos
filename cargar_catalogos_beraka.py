# cargar_catalogos_beraka.py
# Ejecutar desde la carpeta donde está manage.py:
# python manage.py shell < cargar_catalogos_beraka.py

from decimal import Decimal
from eventos.models import (
    AreasEvento,
    CategoriasItem,
    ProductosEvento,
    Servicios,
    TiposEvento,
    ElementosMontaje,
)

print("\n=== CARGANDO CATÁLOGOS BERAKÁ ===\n")

# ------------------------------------------------------------
# 1. ÁREAS
# ------------------------------------------------------------
areas = [
    ("Terraza Principal", 120, "Terraza para eventos y celebraciones.", True),
    ("Terraza Secundaria", 120, "Área exterior para eventos.", True),
    ("Salón Las Orquídeas", 150, "Salón privado para eventos; el paquete de consumo indica 5 horas por $250.", True),
    ("Restaurante", 80, "Espacio dentro del restaurante para eventos por consumo.", True),
    ("Salón VIP", 80, "Salón para eventos privados.", True),
    ("Otro", None, "Área adicional no catalogada.", True),
]

for nombre, capacidad, descripcion, estado in areas:
    AreasEvento.objects.update_or_create(
        nombre=nombre,
        defaults={
            "capacidad": capacidad,
            "descripcion": descripcion,
            "estado": estado,
        },
    )

print(f"Áreas cargadas: {len(areas)}")

# ------------------------------------------------------------
# 2. TIPOS DE EVENTO
# ------------------------------------------------------------
tipos_evento = [
    ("Boda", "Celebración de boda.", True),
    ("Graduación", "Evento de graduación.", True),
    ("Cumpleaños", "Celebración de cumpleaños.", True),
    ("Evento corporativo", "Evento empresarial o corporativo.", True),
    ("Conferencia", "Conferencia o presentación.", True),
    ("Reunión empresarial", "Reunión empresarial.", True),
    ("Baby Shower", "Celebración de baby shower.", True),
    ("XV años", "Celebración de XV años.", True),
    ("Cena", "Cena o evento gastronómico.", True),
    ("Aniversario", "Celebración de aniversario.", True),
    ("Piñata", "Evento infantil de piñata.", True),
    ("Otro", "Otro tipo de evento.", True),
]

for nombre, descripcion, estado in tipos_evento:
    TiposEvento.objects.update_or_create(
        nombre=nombre,
        defaults={"descripcion": descripcion, "estado": estado},
    )

print(f"Tipos de evento cargados: {len(tipos_evento)}")

# ------------------------------------------------------------
# 3. CATEGORÍAS DEL MENÚ
# ------------------------------------------------------------
categorias = {
    "Desayunos": "Desayunos; disponibles también como opción de cena sábados y domingos.",
    "Para picar": "Entradas y opciones para compartir.",
    "Platos fuertes": "Platos principales.",
    "Sopas": "Sopas y preparaciones tradicionales.",
    "Hamburguesas": "Hamburguesas de la casa.",
    "Menú infantil": "Menú para niños menores de 10 años.",
    "Postres": "Postres y opciones dulces.",
    "Bebidas frías": "Bebidas frías.",
    "Refrescantes": "Bebidas refrescantes.",
    "Jugos naturales": "Jugos naturales.",
    "Jugos especiales": "Combinaciones especiales de jugos.",
    "Bebidas con licor": "Vinos y bebidas con licor.",
    "Coctelería": "Cócteles.",
    "Bebidas calientes": "Café y bebidas calientes.",
    "Cervezas": "Cervezas y micheladas.",
    "Cervezas Artesanales": "Cervezas artesanales Cadejo.",
}

categoria_obj = {}

for nombre, descripcion in categorias.items():
    obj, _ = CategoriasItem.objects.update_or_create(
        nombre=nombre,
        defaults={"descripcion": descripcion, "estado": True},
    )
    categoria_obj[nombre] = obj

print(f"Categorías cargadas: {len(categorias)}")

# ------------------------------------------------------------
# 4. MENÚ
# Fuente: MENUUUUU(1).docx
# ------------------------------------------------------------
menu = {
    "Desayunos": [
        ("Típico Beraká", 7.50, "Huevos revueltos con tomatada, frijoles molidos, plátano frito, crema, queso duro y pan."),
        ("Mushroom Bacon Toast", 6.50, "Tostada de masa madre con queso crema y tomate deshidratado, tocino, cebolla morada, hongos frescos y arúgula."),
        ("Panini artesanal Beraká", 7.50, "Pan de mantequilla artesanal con queso crema, eneldo, jamón, pepperoni, mozzarella, arúgula y cebolla morada. Acompañado con papas al horno."),
        ("Bowl Amanecer", 7.00, "Yogurt griego con moras, guineo, fresas, granola y arándanos, con menta fresca."),
        ("Copa de Frutas con Yogurt y Granola", 6.95, "Mezcla de frutas frescas de temporada con yogurt y granola crocante."),
        ("Tostadas francesas con frutos rojos", 7.50, "Pan remojado en leche y huevo, con crema tipo tiramisú, azúcar glass, fresas y arándanos."),
        ("Choricero", 8.50, "Huevos revueltos con tomatada, frijoles molidos, chorizo de tusa de Nahuizalco, aguacate, crema y pan."),
        ("Avocado Toast", 6.95, "Tostada de masa madre con guacamole de la casa, dos huevos estrellados y jamón de pavo."),
        ("Omelette Primavera", 8.25, "Huevos rellenos de queso mozzarella, hongos frescos y espinaca, con tomatada, frijoles molidos, aguacate y pan."),
    ],
    "Para picar": [
        ("Tabla Típica", 5.00, "Frijoles refritos, queso duro, tortillas doradas y guacamole."),
        ("6 oz de chicharrones", 6.00, "Ampliación de la Tabla Típica."),
        ("10 chorizos de tusa", 4.50, "Ampliación de la Tabla Típica."),
    ],
    "Platos fuertes": [
        ("Puyazo (8 oz)", 16.50, None),
        ("Churrasco Tipico (8 oz)", 21.50, "Lomo de aguja a la parrilla con plátano frito, frijoles fritos, chorizo de tusa, vegetales salteados, chimol, aguacate y queso fresco."),
        ("Lomo de Aguja (8 oz)", 20.50, None),
        ("Entraña (8 oz)", 23.50, None),
        ("Mar y Tierra", 25.00, "4 oz de lomo de aguja, 4 oz de pollo a la parrilla y 6 oz de camarones."),
        ("Pechuga al grill", 11.00, "Pechuga de pollo a la parrilla con arroz, vegetales salteados, chimol fresco y dos tortillas."),
        ("Pechuga rellena de queso mozzarella", 13.50, None),
        ("Camarones al Ajo (8 oz)", 17.95, None),
        ("Cuarto de Gallina Asada", 9.00, "Cuarto de gallina asada con arroz, queso fresco, ensalada fresca, curtido de cebolla picante y dos tortillas."),
    ],
    "Sopas": [
        ("Sopa de Res", 10.50, "Sopa tradicional de res con vegetales, curtido de cebolla picante y tortillas."),
        ("Sopa de Pata", 11.00, "Sopa salvadoreña con cortes de res y vegetales, curtido de cebolla picante y tortillas."),
        ("Sopa de Frijoles Rojos", 11.50, "Frijoles rojos con costilla de cerdo, yuca y elote, acompañados de crema y curtido de cebolla picante."),
        ("Sopa de Frijoles Blancos", 11.50, "Frijoles blancos con costilla de cerdo, yuca y elote, acompañados de crema y curtido de cebolla picante."),
        ("Sopa de gallina", 12.00, "Sopa de gallina con vegetales, cuarto de gallina asada, arroz, queso, ensalada y curtido de cebolla picante."),
    ],
    "Hamburguesas": [
        ("La Campestre", 10.50, "6 oz de pechuga de pollo a la parrilla, mozzarella, lechuga, tomate y aderezo de la casa en pan artesanal."),
        ("La Huerta", 9.50, "Hamburguesa vegetariana con hongos salteados, cebolla caramelizada y mozzarella en pan artesanal."),
        ("Especial Beraká", 12.50, "Media libra de carne de res, mozzarella, tocino ahumado, cebolla caramelizada, tomate, arúgula y aderezo especial."),
    ],
    "Menú infantil": [
        ("Hamburguesa", 6.95, "Menú infantil. Incluye papas fritas."),
        ("Nuggets de pollo", 6.95, "Menú infantil. Incluye papas fritas."),
    ],
    "Postres": [
        ("Cheesecake de Frutos Rojos", 4.95, "Cheesecake sobre base crujiente de galleta con mermelada de frutos rojos."),
        ("Cheesecake de chocolate", 4.95, "Cheesecake cremoso sobre base de galleta con cobertura de chocolate."),
        ("Profiteroles de la casa", 4.50, "Profiteroles rellenos de crema de café, bañados en chocolate y acompañados de helado de vainilla."),
        ("Flan de queso horneado", 4.50, "Flan horneado con queso crema y caramelo."),
        ("Budín Beraká", 3.95, "Budín casero suave y húmedo."),
        ("Tiramisú", 4.50, "Bizcocho artesanal humedecido en café con mezcla de queso y vainilla."),
        ("Copa de Helado", 3.95, "Helado de vainilla con mermelada de fresa o chocolate."),
    ],
    "Bebidas frías": [
        ("Ice Latte", 4.00, None),
        ("Affogato", 5.00, None),
        ("Frappé (16 oz)", 5.50, None),
    ],
    "Refrescantes": [
        ("Naranjada", 3.25, None),
        ("Naranjada con soda", 3.75, None),
        ("Agua Freska Cadejo", 2.50, None),
        ("Limonada natural", 3.50, None),
        ("Limonada especial", 3.75, None),
        ("Malteada de piña", 4.50, None),
        ("Agua mineral", 1.75, None),
        ("Sodas", 2.00, None),
        ("Té de Jamaica", 2.75, None),
        ("Horchata", 3.00, None),
        ("Cimarrona", 3.00, None),
    ],
    "Jugos naturales": [
        ("Sandía", 3.50, None),
        ("Papaya", 3.50, None),
        ("Piña", 3.50, None),
        ("Fresa", 3.75, "Hazlo frozen por $1.00 extra."),
    ],
    "Jugos especiales": [
        ("Naranja con piña", 5.00, None),
        ("Naranja con zanahoria", 5.00, None),
        ("Naranja con fresa", 5.00, None),
        ("Naranja con Apio", 5.00, None),
    ],
    "Bebidas con licor": [
        ("Frontera Cabernet Sauvignon Botella", 19.95, None),
        ("Frontera Cabernet Sauvignon Copa", 5.50, None),
        ("Frontera Rose Botella", 19.95, None),
        ("Frontera Rose Copa", 5.50, None),
        ("Barefoot Chardonnay Botella", 25.00, None),
        ("Barefoot Chardonnay Copa", 6.25, None),
        ("Casillero del Diablo Botella", 31.50, None),
        ("Sangría de la casa (1 litro)", 17.50, None),
        ("Copa de sangria Tradicional", 5.90, None),
        ("Fruta Adicional", 0.50, None),
    ],
    "Coctelería": [
        ("Piña Colada", 5.95, None),
        ("Margarita", 5.00, None),
        ("Caipiriña", 5.00, None),
        ("Cuba Libre", 3.75, None),
        ("Mojito", 4.00, None),
        ("Screwdriver", 4.50, None),
        ("Tonga", 5.50, None),
        ("Calimocho", 6.00, None),
    ],
    "Bebidas calientes": [
        ("Americano", 2.75, None),
        ("Espresso", 2.50, None),
        ("Capuccino", 3.75, None),
        ("Capuccino saborizado", 4.95, None),
        ("Latte", 3.50, None),
        ("Masala Chai Latte", 4.00, None),
        ("Te caliente", 2.25, None),
        ("Taza de leche", 2.75, None),
    ],
    "Cervezas": [
        ("Pilsener", 2.75, None),
        ("Corona", 3.50, None),
        ("Michelada Pilsener", 3.75, None),
        ("Coronaa", 3.50, "Nombre conservado tal como aparece en el menú fuente."),
        ("Michelada Corona", 4.50, None),
        ("Suprema", 2.75, None),
        ("Jirafa de Regial 3L + Plato de boca", 17.50, "Incluye 10 chorizos de tusas acompañados de tortillas crujientes."),
    ],
    "Cervezas Artesanales": [
        ("Hija de Pooh", 3.75, "Cerveza rubia ligera, sabores suaves y aroma floral; 4.3% de alcohol."),
        ("Mera belga", 3.75, "Estilo tradicional de belga, ligera y refrescante; 4.8% de alcohol."),
        ("Suegra", None, "Cerveza con amargor intenso y aroma de lúpulo; 5.5% de alcohol. El menú fuente no indica precio."),
    ],
}

productos_insertados = 0

for nombre_categoria, productos in menu.items():
    categoria = categoria_obj[nombre_categoria]

    for nombre, precio, descripcion in productos:
        ProductosEvento.objects.update_or_create(
            nombre=nombre,
            categoria=categoria,
            defaults={
                "descripcion": descripcion,
                "unidad_medida": "unidad",
                "precio_base": Decimal(str(precio)) if precio is not None else None,
                "estado": True,
            },
        )
        productos_insertados += 1

print(f"Productos del menú cargados/actualizados: {productos_insertados}")

# ------------------------------------------------------------
# 5. PRODUCTOS/SERVICIOS QUE USAN LOS PAQUETES
# ------------------------------------------------------------
# Estos no sustituyen el menú general; sirven para cotizaciones
# y para los paquetes VIP / salón / piñata.

catalogo_eventos = [
    ("Servicios de evento", "Entrada de ensalada caprese con pesto de la casa", "Entrada incluida en Paquete VIP.", 3.50, "persona"),
    ("Servicios de evento", "Refil de gaseosa", "Incluido en Paquete VIP.", 2.50, "persona"),
    ("Servicios de evento", "Estación de café", "Incluida en Paquete VIP.", 1.50, "persona"),
    ("Servicios de evento", "Meseros", "Servicio de meseros para evento.", 2.00, "persona"),
    ("Servicios de evento", "Descorche de pastel", "Servicio de descorche de pastel.", 1.00, "persona"),
]

for categoria_nombre, nombre, descripcion, precio, unidad in catalogo_eventos:
    categoria, _ = CategoriasItem.objects.update_or_create(
        nombre=categoria_nombre,
        defaults={
            "descripcion": "Conceptos específicos para eventos y paquetes.",
            "estado": True,
        },
    )

    ProductosEvento.objects.update_or_create(
        nombre=nombre,
        categoria=categoria,
        defaults={
            "descripcion": descripcion,
            "unidad_medida": unidad,
            "precio_base": Decimal(str(precio)),
            "estado": True,
        },
    )

# ------------------------------------------------------------
# 6. SERVICIOS OPCIONALES / FIJOS
# ------------------------------------------------------------
servicios = [
    ("Uso de Salón Las Orquídeas", "Uso del salón por 5 horas.", 250.00),
    ("Servicio de sonido y luces", "Servicio fijo para el evento.", 125.00),
    ("Descorche de boquitas", "Se cobra por cada opción de boquita seleccionada.", 25.00),
    ("DJ", "Servicio de DJ por 5 horas.", 150.00),
    ("Barra libre", "Barra libre por persona.", 10.00),
    ("Hora adicional de evento", "Hora adicional de evento.", 150.00),
    ("Uso de jardín para ceremonia", "Uso de jardín para ceremonia dentro del paquete VIP.", 0.00),
]

for nombre, descripcion, precio in servicios:
    Servicios.objects.update_or_create(
        nombre=nombre,
        defaults={
            "descripcion": descripcion,
            "precio_base": Decimal(str(precio)),
            "estado": True,
        },
    )

print(f"Servicios cargados/actualizados: {len(servicios)}")

# ------------------------------------------------------------
# 7. ELEMENTOS DE MONTAJE
# ------------------------------------------------------------
# Manteles usa $0.38 porque es el valor del último paquete de Piñata
# que se proporcionó.
montajes = [
    ("Base de plato", "Base de plato para montaje.", 1.50, "persona"),
    ("Copa", "Copa de vidrio para montaje.", 1.50, "persona"),
    ("Servilleta de tela", "Servilleta de tela.", 0.50, "persona"),
    ("Manteles", "Manteles para el evento.", 0.38, "persona"),
    ("Florero", "Recipiente para flores; las flores son proporcionadas por los organizadores.", 0.25, "persona"),
]

for nombre, descripcion, precio, unidad in montajes:
    ElementosMontaje.objects.update_or_create(
        nombre=nombre,
        defaults={
            "descripcion": descripcion,
            "precio_base": Decimal(str(precio)),
            "unidad": unidad,
            "estado": True,
        },
    )

print(f"Elementos de montaje cargados/actualizados: {len(montajes)}")

# ------------------------------------------------------------
# 8. PAQUETES DEFINIDOS
# ------------------------------------------------------------
# IMPORTANTE:
# Tu BD/modelos actuales NO tienen una tabla PaquetesEvento.
# Por eso estos datos todavía se mantienen en obtener_paquetes()
# dentro de views.py.
#
# Datos definitivos:
#
# 1) Evento por Consumo
#    - Entrada del menú
#    - Plato fuerte del menú
#    - Bebida del menú
#    - Postre del menú
#    - Espacio dentro del restaurante sin costo adicional
#    - 10% de propina
#
# 2) Evento por Consumo + Salón Las Orquídeas
#    - Entrada del menú
#    - Plato fuerte del menú
#    - Bebida del menú
#    - Postre del menú
#    - 5 horas de Salón Las Orquídeas
#    - Aire acondicionado
#    - Sonido profesional
#    - Proyector
#    - Mesas y sillas
#    - Salón: $250 / 5 horas
#    - 10% de propina
#
# 3) Paquete VIP
#    - Entrada: Ensalada Caprese con pesto de la casa
#    - Plato fuerte: opción pollo / carne / vegetariana
#    - Refil de gaseosa
#    - Estación de café
#    - Base de plato + copa
#    - Manteles
#    - Servilletas de tela
#    - Florero
#    - Descorche de pastel
#    - Meseros exclusivos
#    - Uso de jardín para ceremonia
#    - Vegetariano: $33.75 p/p
#    - Pollo: $37.25 p/p
#    - Carne: $40.75 p/p
#    - Sonido y luces: $125 fijo
#    - 10% de propina
#
# 4) Paquete Piñata
#    - Hamburguesa Jr o Nuggets: $6.95 p/p
#    - Refill de gaseosa: $2.50 p/p
#    - Estación de café: $1.50 p/p
#    - Meseros: $2.00 p/p
#    - Descorche de pastel: $1.00 p/p
#    - Manteles: $0.38 p/p
#    - Uso de salón 5 horas: $100 fijo
#    - Costo por persona indicado: $14.33
#
# El Paquete Piñata queda registrado aquí como especificación
# hasta que agreguemos las tablas de paquetes y sus relaciones.

print("\n=== CARGA TERMINADA ===")
print("Revisa la base antes de modificar datos existentes.")
print("Los paquetes todavía son datos de aplicación porque no existe")
print("una tabla PaquetesEvento en los modelos actuales.")
