from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TourViewSet, ReservaViewSet, SubcategoriaViewSet, TarifaFechaTourViewSet, TourImagenViewSet, BannerPromocionalViewSet

router = DefaultRouter()
router.register(r'tours', TourViewSet, basename='tour')
router.register(r'reservas', ReservaViewSet)
router.register(r'subcategorias', SubcategoriaViewSet, basename='subcategorias')
router.register(r'tarifas-especiales', TarifaFechaTourViewSet)
router.register(r'tour-imagenes', TourImagenViewSet)
router.register(r'banners', BannerPromocionalViewSet, basename='banner')

urlpatterns = [
    path('api/', include(router.urls)),
]