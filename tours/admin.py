from django.contrib import admin
from .models import Tour, Reserva

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    # Campos que se verán en la lista general del panel
    list_display = ('titulo', 'destino_slug', 'categoria', 'precio', 'activo', 'es_popular')
    
    # Filtros laterales en el panel de administración
    list_filter = ('destino_slug', 'categoria', 'activo', 'es_popular')
    
    # Campos que se podrán buscar directamente en la barra de búsqueda del admin
    search_fields = ('titulo', 'descripcion')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('nombre_cliente', 'tour', 'fecha_viaje', 'estado_pago', 'total_pagar')
    list_filter = ('estado_pago', 'fecha_viaje')
    search_fields = ('nombre_cliente', 'email_cliente', 'transaccion_id')