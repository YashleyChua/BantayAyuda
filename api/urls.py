from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HouseholdViewSet, DisasterEventViewSet, DamageAssessmentViewSet, generate_sms

router = DefaultRouter()
router.register(r'households', HouseholdViewSet, basename='household')
router.register(r'disasters', DisasterEventViewSet, basename='disaster')
router.register(r'assessments', DamageAssessmentViewSet, basename='assessment')

urlpatterns = [
    path('', include(router.urls)),
    path('generate-sms/', generate_sms, name='generate-sms'),
]

