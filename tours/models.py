from django.db import models

class Tour(models.Model):
    CATEGORIAS = [
        ('playas-islas', 'Playas & Islas'),
        ('hoteles-posadas', 'Hoteles & Posadas'),
        ('viajes-nacionales', 'Viajes nacionales'),
        ('viajes-internacionales', 'Viajes internacionales'),
        ('botes-privados', 'Botes & Privados'),
        ('planes-familias', 'Planes para familias'),
        ('experiencia', 'Tour y Experiencias'),
        ('yate', 'Renta de Botes y Yates'),
        ('hotel', 'Hoteles'),
        ('transporte', 'Transportes'),
        ('internacional', 'Tours Internacionales'),
        ('a_medida', 'A Medida (Preguntar)'),
    ]

    # Ciudades y destinos soportados
    DESTINOS_CHOICES = [
        ('cartagena', 'Cartagena'),
        ('san_andres', 'San Andrés'),
        ('santa_marta', 'Santa Marta'),
        ('medellin', 'Medellín'),
        ('eje_cafetero', 'Eje Cafetero'),
        ('bogota', 'Bogotá'),
        ('cancun', 'Cancún (Internacional)'),
        ('madrid', 'Madrid (Internacional)'),
    ]

    REGIONES_CHOICES = [
        ('colombia', 'Colombia'),
        ('internacional', 'Internacional'),
    ]

    titulo = models.CharField(max_length=200)
    dias = models.CharField(max_length=100)
    precio = models.IntegerField()  # Guardado como entero
    imagen = models.ImageField(upload_to='tours_images/')
    descripcion = models.TextField()
    incluye = models.JSONField(default=list)
    itinerario = models.JSONField(default=list)
    activo = models.BooleanField(default=True)

    categoria = models.CharField(max_length=50, choices=CATEGORIAS, default='experiencia')
    destino_slug = models.CharField(max_length=50, choices=DESTINOS_CHOICES, default='cartagena')
    region = models.CharField(max_length=20, choices=REGIONES_CHOICES, default='colombia')
    es_popular = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.titulo} ({self.get_destino_slug_display()})"


class Reserva(models.Model):
    ESTADOS_PAGO = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('rechazado', 'Rechazado'),
    ]

    # Relacionamos la reserva con el Tour
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reservas')
    
    # Datos del cliente
    nombre_cliente = models.CharField(max_length=150)
    email_cliente = models.EmailField()
    telefono = models.CharField(max_length=20)
    
    # Datos del viaje
    fecha_viaje = models.DateField()
    viajeros = models.IntegerField()
    total_pagar = models.IntegerField()
    
    # Control de pago
    estado_pago = models.CharField(max_length=20, choices=ESTADOS_PAGO, default='pendiente')
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    
    # Aquí guardaremos el ID de la transacción de MercadoPago o Stripe
    transaccion_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Reserva de {self.nombre_cliente} - {self.tour.titulo} ({self.estado_pago})"



class BannerPromocional(models.Model):
    seccion = models.CharField(max_length=100, default='home_viaja_medida', unique=True)
    imagen_desktop = models.ImageField(upload_to='banners_images/')
    imagen_mobile = models.ImageField(upload_to='banners_images/', blank=True, null=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Banner: {self.seccion}"

class TourImagen(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='galeria')
    imagen = models.ImageField(upload_to='tours_galeria/')
    
    def __str__(self):
        return f"Imagen para {self.tour.titulo}"