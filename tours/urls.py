from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TourViewSet, ReservaViewSet, SubcategoriaViewSet, TarifaFechaTourViewSet, TourImagenViewSet, BannerPromocionalViewSet, FechaBloqueadaViewSet, CategoriaViewSet, DestinoViewSet, RecomendacionViewSet

router = DefaultRouter()
router.register(r'tours', TourViewSet, basename='tour')
router.register(r'reservas', ReservaViewSet)
router.register(r'subcategorias', SubcategoriaViewSet, basename='subcategorias')
router.register(r'tarifas-especiales', TarifaFechaTourViewSet)
router.register(r'tour-imagenes', TourImagenViewSet)
router.register(r'banners', BannerPromocionalViewSet, basename='banner')
router.register(r'fechas-bloqueadas', FechaBloqueadaViewSet)
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'destinos', DestinoViewSet, basename='destino')
router.register(r'recomendaciones', RecomendacionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]