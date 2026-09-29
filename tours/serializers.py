from rest_framework import serializers
from .models import Tour, Reserva

class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = '__all__' # Exporta todos los campos (id, titulo, precio, incluye, itinerario, etc.)

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