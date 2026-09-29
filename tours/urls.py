from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TourViewSet, ReservaViewSet

router = DefaultRouter()
router.register(r'tours', TourViewSet, basename='tour')
router.register(r'reservas', ReservaViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]