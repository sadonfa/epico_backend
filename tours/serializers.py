from rest_framework import serializers
from .models import Tour, Reserva, TourImagen, Subcategoria, TarifaFechaTour, BannerPromocional, FechaBloqueadaTour, Categoria, Destino, Recomendacion



class TourImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourImagen
        fields = ['id', 'imagen']

class TarifaFechaTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = TarifaFechaTour
        fields = ['id', 'tour', 'fecha_inicio', 'fecha_fin', 'precio_especial']

class SubcategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategoria
        fields = '__all__'

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class DestinoSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(required=False, allow_blank=True)
    
    class Meta:
        model = Destino
        fields = '__all__'

class FechaBloqueadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FechaBloqueadaTour
        fields = ['id', 'tour', 'fecha_inicio', 'fecha_fin', 'motivo']

class TourSerializer(serializers.ModelSerializer):
    # Esto inyectará una lista llamada 'galeria' con todas las fotos adicionales
    fechas_bloqueadas = FechaBloqueadaSerializer(many=True, read_only=True)
    galeria = TourImagenSerializer(many=True, read_only=True)
    imagen = serializers.ImageField(required=False, allow_null=True)
    tarifas_especiales = TarifaFechaTourSerializer(many=True, read_only=True)
    subcategoria_nombre = serializers.ReadOnlyField(source='subcategoria.nombre')
    region = serializers.ReadOnlyField(source='destino_slug.region')
    # destino_nombre = serializers.ReadOnlyField(source='destino_slug.nombre')
    destino_slug_str = serializers.ReadOnlyField(source='destino_slug.slug')

    class Meta:
        model = Tour
        fields = '__all__'


class BannerPromocionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannerPromocional
        fields = '__all__'


class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = '__all__'


class ReservaSerializer(serializers.ModelSerializer):
    # Esto agrega el título del tour solo para lectura, sin dañar el POST que ya hicimos
    nombre_tour = serializers.CharField(source='tour.titulo', read_only=True)

    class Meta:
        model = Reserva
        fields = '__all__'

class RecomendacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recomendacion
        fields = '__all__'