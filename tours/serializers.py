from rest_framework import serializers
from .models import Tour, Reserva, TourImagen

class TourImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourImagen
        fields = ['id', 'imagen']

class TourSerializer(serializers.ModelSerializer):
    # Esto inyectará una lista llamada 'galeria' con todas las fotos adicionales
    galeria = TourImagenSerializer(many=True, read_only=True)
    imagen = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Tour
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