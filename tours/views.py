from rest_framework.permissions import IsAuthenticated, AllowAny
import requests
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Tour, Reserva
from .serializers import TourSerializer, ReservaSerializer
import uuid
import hashlib


class TourViewSet(viewsets.ModelViewSet):
    serializer_class = TourSerializer
    # 1. Función inteligente que decide qué lista devolver
    def get_queryset(self):
        # Si la petición tiene el token de administrador de React
        if self.request.user.is_authenticated:
            return Tour.objects.all().order_by('-id') # Devuelve TODOS
        
        # Si es un cliente normal desde la web pública
        return Tour.objects.filter(activo=True) # Devuelve SOLO LOS ACTIVOS

    # 2. Seguridad: Quién puede hacer qué
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # El público puede ver la lista de tours
            permission_classes = [AllowAny]
        else:
            # Solo tú (el admin) puedes crear, editar o borrar
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

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