from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TourViewSet, ReservaViewSet, SubcategoriaViewSet

router = DefaultRouter()
router.register(r'tours', TourViewSet, basename='tour')
router.register(r'reservas', ReservaViewSet)
router.register(r'subcategorias', SubcategoriaViewSet, basename='subcategorias')

urlpatterns = [
    path('api/', include(router.urls)),
]