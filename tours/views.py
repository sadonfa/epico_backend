from rest_framework.permissions import IsAuthenticated, AllowAny
import requests
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Tour, Reserva, TourImagen
from .serializers import TourSerializer, ReservaSerializer
import uuid
import hashlib
from django.db import models


class TourViewSet(viewsets.ModelViewSet):
    serializer_class = TourSerializer

    # 1. Función inteligente que decide qué lista devolver
    def get_queryset(self):
        # Si la petición tiene el token de administrador de React
        if self.request.user.is_authenticated:
            queryset = Tour.objects.all().order_by('-id')  # Devuelve TODOS
        else:
            queryset = Tour.objects.filter(activo=True)  # Devuelve SOLO LOS ACTIVOS

        # 1. Filtrar por categoría si viene en la URL
        categoria = self.request.query_params.get('categoria')
        if categoria:
            queryset = queryset.filter(categoria=categoria)

        # 2. Filtrar por región si viene en la URL o parámetros
        region = self.request.query_params.get('region')
        if region:
            queryset = queryset.filter(region=region)

        return queryset

    # 2. Seguridad: Quién puede hacer qué
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    # 3. Crear tour y procesar múltiples imágenes de la galería
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tour = serializer.save()

        # Capturamos las múltiples imágenes enviadas desde el FormData de React
        imagenes_galeria = request.FILES.getlist('galeria_imagenes')
        for img_file in imagenes_galeria:
            TourImagen.objects.create(tour=tour, imagen=img_file)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # 4. Actualizar tour y añadir nuevas imágenes a la galería si se seleccionaron
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        tour = serializer.save()

        # Procesar imágenes adicionales de la galería en la actualización
        imagenes_galeria = request.FILES.getlist('galeria_imagenes')
        if imagenes_galeria:
            for img_file in imagenes_galeria:
                TourImagen.objects.create(tour=tour, imagen=img_file)

        return Response(serializer.data)

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer

    def get_permissions(self):
        if self.action == 'create':
            # Cualquiera puede crear una reserva (Comprar)
            permission_classes = [AllowAny]
        else:
            # Solo los administradores logueados pueden ver o editar (Dashboard)
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        datos = request.data
        token_tarjeta = datos.get('token_tarjeta')

        # 1. Configurar tus llaves y Secret de Wompi
        wompi_priv_key = (
            'prv_test_cPKw6fpIumQpGdVp8X4PbifDwdqbohFA'  # Tu llave privada (prv_test_...)
        )
        wompi_pub_key = (
            'pub_test_695VEqaqdswPQbesc5iw3sFJL8vn15RV'  # Tu llave pública
        )
        wompi_integrity_secret = 'test_integrity_GV6cFH2HEoQYMrtzV2XEf8AjcotxUr8p'  # Lo encuentras en el panel bajo "Secret de integridad"

        # 2. Pedir el acceptance_token legal
        url_merchant = f'https://sandbox.wompi.co/v1/merchants/{wompi_pub_key}'
        respuesta_merchant = requests.get(url_merchant)
        merchant_data = respuesta_merchant.json()
        acceptance_token = merchant_data['data']['presigned_acceptance'][
            'acceptance_token'
        ]

        # 3. Preparar los datos del cobro
        monto_en_centavos = int(datos['total_pagar']) * 100
        moneda = 'COP'
        referencia = f"reserva_epico_{uuid.uuid4().hex[:8]}"

        # 4. GENERAR LA FIRMA DE INTEGRIDAD (SHA-256)
        cadena_firma = f"{referencia}{monto_en_centavos}{moneda}{wompi_integrity_secret}"
        
        # --- CHISMOSO DE LA FIRMA ---
        print("--- DEBUG FIRMA ---")
        print("Cadena a encriptar:", cadena_firma)
        print("-------------------")
        
        firma_sha256 = hashlib.sha256(cadena_firma.encode('utf-8')).hexdigest()

        # 5. Armar el Payload completo con la firma
        payload = {
            'acceptance_token': acceptance_token,
            'amount_in_cents': monto_en_centavos,
            'currency': moneda,
            'signature': firma_sha256,  # <--- FIRMA REQUERIDA
            'customer_email': datos['email_cliente'],
            'payment_method': {
                'type': 'CARD',
                'token': token_tarjeta,
                'installments': 1,
            },
            'reference': referencia,
        }

        headers = {'Authorization': f'Bearer {wompi_priv_key}'}

        # 6. Hacer la transacción en Wompi
        url_wompi = 'https://sandbox.wompi.co/v1/transactions'
        respuesta_wompi = requests.post(url_wompi, json=payload, headers=headers)
        resultado = respuesta_wompi.json()

        # Chismoso para ver exactamente qué nos responde Wompi en la consola
        print("--- RESPUESTA WOMPI ---")
        print("CÓDIGO HTTP:", respuesta_wompi.status_code)
        print("DATOS:", resultado)
        print("-----------------------")

        # 7. Evaluar el resultado
        estado_transaccion = resultado.get('data', {}).get('status', '')
        if respuesta_wompi.status_code in [200, 201] and estado_transaccion in ['APPROVED', 'PENDING']:
            nueva_reserva = Reserva.objects.create(
                tour_id=datos['tour'],
                nombre_cliente=datos['nombre_cliente'],
                email_cliente=datos['email_cliente'],
                telefono=datos['telefono'],
                fecha_viaje=datos['fecha_viaje'],
                viajeros=datos['viajeros'],
                total_pagar=datos['total_pagar'],
                estado_pago='pagado',
                transaccion_id=resultado['data']['id'],
            )

            return Response(
                {
                    'mensaje': 'Reserva confirmada exitosamente',
                    'transaccion_id': resultado['data']['id'],
                },
                status=status.HTTP_201_CREATED,
            )
        else: # <--- El else debe ir alineado con el if
            error_msg = 'El pago fue rechazado por el banco' # <--- Esto lleva sangría (tabulación)
            
            if 'data' in resultado and 'status_message' in resultado['data']:
                error_msg = resultado['data']['status_message']

            return Response(
                {'error': error_msg, 'detalles': resultado},
                status=status.HTTP_400_BAD_REQUEST,
            )