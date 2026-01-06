from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SessionViewSet, ExerciseViewSet

router = DefaultRouter()
router.register(r'sessions', SessionViewSet)
router.register(r'exercises', ExerciseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
