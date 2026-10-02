# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AreasEvento(models.Model):
    area_id = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=100)
    capacidad = models.IntegerField(blank=True, null=True)
    descripcion = models.CharField(max_length=250, blank=True, null=True)
    estado = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'areas_evento'


class CategoriasItem(models.Model):
    categoria_id = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=100)
    descripcion = models.CharField(max_length=250, blank=True, null=True)
    estado = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'categorias_item'


class Clientes(models.Model):
    cliente_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    correo = models.CharField(max_length=150, blank=True, null=True)
    direccion = models.CharField(max_length=250, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'clientes'


class ConfirmacionesEvento(models.Model):
    confirmacion_id = models.AutoField(primary_key=True)
    evento = models.ForeignKey('Eventos', models.DB_CASCADE)
    concepto = models.CharField(max_length=150)
    respuesta = models.CharField(max_length=250, blank=True, null=True)
    fecha_confirmacion = models.DateField(blank=True, null=True)
    confirmado_por = models.CharField(max_length=150, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'confirmaciones_evento'


class Cotizaciones(models.Model):
    cotizacion_id = models.AutoField(primary_key=True)
    evento = models.ForeignKey('Eventos', models.DO_NOTHING)
    numero_cotizacion = models.CharField(unique=True, max_length=50)
    fecha = models.DateField()
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    porcentaje_propina = models.DecimalField(max_digits=5, decimal_places=2)
    monto_propina = models.DecimalField(max_digits=12, decimal_places=2)
    descuento = models.DecimalField(max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    estado = models.CharField(max_length=50)
    observaciones = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'cotizaciones'


class DecoracionesEvento(models.Model):
    decoracion_id = models.AutoField(primary_key=True)
    evento = models.ForeignKey('Eventos', models.DB_CASCADE)
    descripcion = models.TextField()
    ubicacion = models.CharField(max_length=250, blank=True, null=True)
    hora_inicio = models.TimeField(blank=True, null=True)
    hora_fin = models.TimeField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'decoraciones_evento'


class DetalleCotizacion(models.Model):
    detalle_cotizacion_id = models.AutoField(primary_key=True)
    cotizacion = models.ForeignKey(Cotizaciones, models.DB_CASCADE)
    producto_evento = models.ForeignKey('ProductosEvento', models.DO_NOTHING, blank=True, null=True)
    elemento_montaje = models.ForeignKey('ElementosMontaje', models.DO_NOTHING, blank=True, null=True)
    concepto = models.CharField(max_length=250)
    descripcion = models.TextField(blank=True, null=True)
    cantidad = models.DecimalField(max_digits=12, decimal_places=2)
    unidad = models.CharField(max_length=50, blank=True, null=True)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detalle_cotizacion'


class DetallesEvento(models.Model):
    detalle_evento_id = models.AutoField(primary_key=True)
    evento = models.ForeignKey('Eventos', models.DB_CASCADE)
    producto_evento = models.ForeignKey('ProductosEvento', models.DO_NOTHING)
    cantidad = models.DecimalField(max_digits=12, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detalles_evento'


class ElementosMontaje(models.Model):
    elemento_montaje_id = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    precio_base = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    unidad = models.CharField(max_length=50, blank=True, null=True)
    estado = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'elementos_montaje'


class Empleados(models.Model):
    empleado_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    cargo = models.CharField(max_length=100, blank=True, null=True)
    estado = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'empleados'


class EstacionesEvento(models.Model):
    estacion_id = models.AutoField(primary_key=True)
    evento = models.ForeignKey('Eventos', models.DB_CASCADE)
    tipo = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=250, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'estaciones_evento'


class EstadosEvento(models.Model):
    estado_id = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=50)
    descripcion = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'estados_evento'


class Eventos(models.Model):
    evento_id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Clientes, models.DO_NOTHING)
    tipo_evento = models.ForeignKey('TiposEvento', models.DO_NOTHING)
    area = models.ForeignKey(AreasEvento, models.DO_NOTHING)
    estado = models.ForeignKey(EstadosEvento, models.DO_NOTHING)
    fecha_evento = models.DateField()
    hora_inicio = models.TimeField(blank=True, null=True)
    hora_fin = models.TimeField(blank=True, null=True)
    hora_inicio_montaje = models.TimeField(blank=True, null=True)
    cantidad_adultos = models.IntegerField()
    cantidad_ninos = models.IntegerField()
    total_invitados = models.IntegerField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'eventos'


class MesasEvento(models.Model):
    mesa_evento_id = models.AutoField(primary_key=True)
    evento = models.ForeignKey(Eventos, models.DB_CASCADE)
    tipo_mesa = models.ForeignKey('TiposMesa', models.DO_NOTHING)
    cantidad = models.IntegerField()
    personas_por_mesa = models.IntegerField(blank=True, null=True)
    ubicacion = models.CharField(max_length=150, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mesas_evento'


class MetodosPago(models.Model):
    metodo_pago_id = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=100)
    descripcion = models.CharField(max_length=250, blank=True, null=True)
    estado = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'metodos_pago'


class MontajesEvento(models.Model):
    montaje_evento_id = models.AutoField(primary_key=True)
    evento = models.ForeignKey(Eventos, models.DB_CASCADE)
    elemento_montaje = models.ForeignKey(ElementosMontaje, models.DO_NOTHING)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    color = models.CharField(max_length=100, blank=True, null=True)
    ubicacion = models.CharField(max_length=150, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'montajes_evento'


class ObservacionesEvento(models.Model):
    observacion_id = models.AutoField(primary_key=True)
    evento = models.ForeignKey(Eventos, models.DB_CASCADE)
    tipo = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.TextField()
    fecha_registro = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'observaciones_evento'


class Pagos(models.Model):
    pago_id = models.AutoField(primary_key=True)
    evento = models.ForeignKey(Eventos, models.DO_NOTHING)
    metodo_pago = models.ForeignKey(MetodosPago, models.DO_NOTHING)
    fecha_pago = models.DateField()
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    tipo_pago = models.CharField(max_length=50, blank=True, null=True)
    numero_referencia = models.CharField(max_length=100, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'pagos'


class PendientesEvento(models.Model):
    pendiente_id = models.AutoField(primary_key=True)
    evento = models.ForeignKey(Eventos, models.DB_CASCADE)
    descripcion = models.CharField(max_length=250)
    responsable = models.CharField(max_length=150, blank=True, null=True)
    fecha_limite = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=50)
    fecha_completado = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pendientes_evento'


class ProductosEvento(models.Model):
    producto_evento_id = models.AutoField(primary_key=True)
    categoria = models.ForeignKey(CategoriasItem, models.DO_NOTHING)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    unidad_medida = models.CharField(max_length=50, blank=True, null=True)
    precio_base = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    estado = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'productos_evento'


class Proveedores(models.Model):
    proveedor_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    correo = models.CharField(max_length=150, blank=True, null=True)
    servicio = models.CharField(max_length=150, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    estado = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'proveedores'


class Servicios(models.Model):
    servicio_id = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    precio_base = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    estado = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'servicios'


class ServiciosProveedorEvento(models.Model):
    servicio_proveedor_id = models.AutoField(primary_key=True)
    evento = models.ForeignKey(Eventos, models.DB_CASCADE)
    proveedor = models.ForeignKey(Proveedores, models.DO_NOTHING)
    servicio = models.ForeignKey(Servicios, models.DO_NOTHING)
    costo = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    estado = models.CharField(max_length=50)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'servicios_proveedor_evento'


class TiposEvento(models.Model):
    tipo_evento_id = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=100)
    descripcion = models.CharField(max_length=250, blank=True, null=True)
    estado = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'tipos_evento'


class TiposMesa(models.Model):
    tipo_mesa_id = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=100)
    capacidad = models.IntegerField(blank=True, null=True)
    descripcion = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipos_mesa'


# ============================================================
# PAQUETES DE EVENTOS
# ============================================================

class PaquetesEvento(models.Model):

    id_paquete = models.AutoField(
        primary_key=True
    )

    tipo_evento = models.ForeignKey(
        "TiposEvento",
        on_delete=models.PROTECT,
        related_name="paquetes"
    )

    nombre = models.CharField(
        max_length=150
    )

    descripcion = models.TextField(
        blank=True,
        null=True
    )

    precio_base = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    cantidad_personas_base = models.PositiveIntegerField(
        default=1
    )

    activo = models.BooleanField(
        default=True
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        db_table = "paquetes_evento"

        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


# ============================================================
# PRODUCTOS DEL PAQUETE
# ============================================================

class PaqueteProductos(models.Model):

    id_paquete_producto = models.AutoField(
        primary_key=True
    )

    paquete = models.ForeignKey(
        PaquetesEvento,
        on_delete=models.CASCADE,
        related_name="productos"
    )

    producto = models.ForeignKey(
        "ProductosEvento",
        on_delete=models.PROTECT,
        related_name="paquetes"
    )

    cantidad = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1
    )

    obligatorio = models.BooleanField(
        default=True
    )

    class Meta:

        db_table = "paquete_productos"

        unique_together = (
            "paquete",
            "producto",
        )

    def __str__(self):
        return f"{self.paquete.nombre} - {self.producto.nombre}"


# ============================================================
# SERVICIOS DEL PAQUETE
# ============================================================

class PaqueteServicios(models.Model):

    id_paquete_servicio = models.AutoField(
        primary_key=True
    )

    paquete = models.ForeignKey(
        PaquetesEvento,
        on_delete=models.CASCADE,
        related_name="servicios"
    )

    servicio = models.ForeignKey(
        "Servicios",
        on_delete=models.PROTECT,
        related_name="paquetes"
    )

    cantidad = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1
    )

    obligatorio = models.BooleanField(
        default=True
    )

    class Meta:

        db_table = "paquete_servicios"

        unique_together = (
            "paquete",
            "servicio",
        )

    def __str__(self):
        return f"{self.paquete.nombre} - {self.servicio.nombre}"


# ============================================================
# MONTAJE DEL PAQUETE
# ============================================================

class PaqueteMontaje(models.Model):

    id_paquete_montaje = models.AutoField(
        primary_key=True
    )

    paquete = models.ForeignKey(
        PaquetesEvento,
        on_delete=models.CASCADE,
        related_name="montajes"
    )

    elemento = models.ForeignKey(
        "ElementosMontaje",
        on_delete=models.PROTECT,
        related_name="paquetes"
    )

    cantidad = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1
    )

    obligatorio = models.BooleanField(
        default=True
    )

    class Meta:

        db_table = "paquete_montaje"

        unique_together = (
            "paquete",
            "elemento",
        )

    def __str__(self):
        return f"{self.paquete.nombre} - {self.elemento.nombre}"