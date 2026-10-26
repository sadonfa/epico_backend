from django.db import models
from django.utils.text import slugify

class Subcategoria(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True, help_text="Ej: playas-islas, experiencias")

    def save(self, *args, **kwargs):
        if not self.slug:
            # Genera un slug limpio eliminando caracteres especiales como '&'
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre


class Destino(models.Model):
    REGIONES_CHOICES = [
        ('colombia', 'Colombia'),
        ('internacional', 'Internacional'),
    ]

    nombre = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True, help_text="Ej: cartagena, san_andres")
    region = models.CharField(max_length=50, choices=REGIONES_CHOICES, default='colombia')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Destino"
        verbose_name_plural = "Destinos"

    def __str__(self):
        return f"{self.nombre} ({self.get_region_display()})"


class Tour(models.Model):
   
    titulo = models.CharField(max_length=200)
    dias = models.CharField(max_length=100)
    precio = models.IntegerField()  # Guardado como entero
    precio_ninos = models.IntegerField(null=True, blank=True)
    imagen = models.ImageField(upload_to='tours_images/')
    descripcion = models.TextField()
    incluye = models.JSONField(default=list)
    no_incluye = models.JSONField(default=list)
    itinerario = models.JSONField(default=list)
    activo = models.BooleanField(default=True)
    edad_maxima_nino = models.IntegerField(default=10, help_text="Edad máxima para aplicar tarifa de niño")
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='tours'
    )
    subcategoria = models.ForeignKey(
        Subcategoria, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='tours'
    )
    destino_slug = models.ForeignKey(
        Destino, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='tours'
    )
    ubicacion = models.CharField(
        max_length=150, 
        blank=True, 
        null=True, 
        help_text="Ej: Isla Barú, Playa Blanca, Centro Histórico"
    )
    es_popular = models.BooleanField(default=False)
    es_paquete = models.BooleanField(default=False, help_text="Marcar si es un paquete turístico completo")

    def __str__(self):
        nombre_destino = self.destino_slug.nombre if self.destino_slug else "Sin destino"
        return f"{self.titulo} ({nombre_destino})"





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
    imagen_desktop = models.ImageField(upload_to='banners/', null=True, blank=True)
    imagen_mobile = models.ImageField(upload_to='banners/', null=True, blank=True)
    actualizado_el = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Banner Promocional #{self.id}"

class TourImagen(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='galeria')
    imagen = models.ImageField(upload_to='tours_galeria/')
    
    def __str__(self):
        return f"Imagen para {self.tour.titulo}"


class TarifaFechaTour(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='tarifas_especiales')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    precio_especial = models.IntegerField() # Nuevo precio en COP para este rango

    def __str__(self):
        return f"{self.tour.titulo} ({self.fecha_inicio} al {self.fecha_fin}): ${self.precio_especial}"

class FechaBloqueadaTour(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='fechas_bloqueadas')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    motivo = models.CharField(max_length=150, blank=True, null=True, help_text="Ej: Mantenimiento, Cupo Lleno")

    def __str__(self):
        return f"{self.tour.titulo} - Cerrado: {self.fecha_inicio} a {self.fecha_fin}"


class Recomendacion(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    imagen = models.ImageField(upload_to='recomendaciones_images/')
    extracto = models.TextField(help_text="Resumen corto que se muestra en la tarjeta")
    contenido = models.TextField(help_text="Contenido completo del artículo o recomendación")
    fecha_publicacion = models.DateField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo