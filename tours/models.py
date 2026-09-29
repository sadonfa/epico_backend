from django.db import models

class Tour(models.Model):

    CATEGORIAS = [
        ('experiencia', 'Tour y Experiencias'),
        ('yate', 'Renta de Botes y Yates'),
        ('hotel', 'Hoteles'),
        ('transporte', 'Transportes'),
        ('internacional', 'Tours Internacionales'),
        ('a_medida', 'A Medida (Preguntar)'),
    ]

    titulo = models.CharField(max_length=200)
    dias = models.CharField(max_length=100)
    precio = models.IntegerField()  # Guardado como entero para calcular los multiplicadores de viajeros
    imagen = models.ImageField(upload_to='tours_images/')  # Ruta o nombre de la imagen
    descripcion = models.TextField()
    incluye = models.JSONField(default=list)      # Guardará la lista de lo que incluye
    itinerario = models.JSONField(default=list)  # Guardará el listado de horas y actividades
    activo = models.BooleanField(default=True)

    categoria = models.CharField(max_length=50, choices=CATEGORIAS, default='experiencia')
    es_popular = models.BooleanField(default=False) # Si es True, saldrá en el Home


    def __str__(self):
        return self.titulo


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