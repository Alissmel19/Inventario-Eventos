# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Adicionales(models.Model):
    id_adicional = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'adicionales'


class AreasEvento(models.Model):
    area_id = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=100)
    capacidad = models.IntegerField(blank=True, null=True)
    descripcion = models.CharField(max_length=250, blank=True, null=True)
    estado = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'areas_evento'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Bebidas(models.Model):
    id_bebida = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=200, blank=True, null=True)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    ingredientes = models.CharField(max_length=200, blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    categoria = models.ForeignKey('CategoriasItem', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bebidas'


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


class Cortesia(models.Model):
    id_cortesia = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cortesia'


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


class DetalleHospedaje(models.Model):
    id_detalle_hospedaje = models.IntegerField(primary_key=True)
    check_in = models.TimeField(blank=True, null=True)
    check_out = models.TimeField(blank=True, null=True)
    id_hospedaje = models.ForeignKey('Hospedaje', models.DO_NOTHING, db_column='id_hospedaje', blank=True, null=True)
    id_habitaciones = models.ForeignKey('Habitaciones', models.DO_NOTHING, db_column='id_habitaciones', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detalle_hospedaje'


class DetallesEvento(models.Model):
    detalle_evento_id = models.AutoField(primary_key=True)
    evento = models.ForeignKey('Eventos', models.DB_CASCADE)
    producto_evento_id = models.IntegerField()
    cantidad = models.DecimalField(max_digits=12, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detalles_evento'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


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
    tipo = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=250, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)

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


class Habitaciones(models.Model):
    id_habitaciones = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    capacidad = models.IntegerField(blank=True, null=True)
    servicios_incluidos = models.CharField(max_length=200, blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'habitaciones'


class Hospedaje(models.Model):
    id_hospedaje = models.IntegerField(primary_key=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    cliente = models.ForeignKey(Clientes, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hospedaje'


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


class PaquetesEvento(models.Model):
    id_paquete = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    min_personas = models.IntegerField(blank=True, null=True)
    que_incluye = models.TextField(blank=True, null=True)
    modalidad_pago = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'paquetes_evento'


class Platillo(models.Model):
    id_platillo = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.CharField(max_length=300, blank=True, null=True)
    ingredientes = models.CharField(max_length=200, blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    categoria = models.ForeignKey(CategoriasItem, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'platillo'


class PlatilloAdicional(models.Model):
    pk = models.CompositePrimaryKey('id_platillo', 'id_adicional')
    id_platillo = models.ForeignKey(Platillo, models.DO_NOTHING, db_column='id_platillo')
    id_adicional = models.ForeignKey(Adicionales, models.DO_NOTHING, db_column='id_adicional')

    class Meta:
        managed = False
        db_table = 'platillo_adicional'


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
    id_servicio = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=300, blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    estado = models.BooleanField(blank=True, null=True)
    id_paquete = models.ForeignKey(PaquetesEvento, models.DO_NOTHING, db_column='id_paquete', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'servicios'


class ServiciosAdicionales(models.Model):
    id_servicio_adicional = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'servicios_adicionales'


class ServiciosOpcionales(models.Model):
    id_servicio_opcional = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    medida = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'servicios_opcionales'


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
