from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TourViewSet, ReservaViewSet, SubcategoriaViewSet, TarifaFechaTourViewSet

router = DefaultRouter()
router.register(r'tours', TourViewSet, basename='tour')
router.register(r'reservas', ReservaViewSet)
router.register(r'subcategorias', SubcategoriaViewSet, basename='subcategorias')
router.register(r'tarifas-especiales', TarifaFechaTourViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]