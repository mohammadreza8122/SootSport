from django.urls import path
from .views import SportFacilityListAPIView, SportFacilityDetailAPIView

app_name = 'provider'

urlpatterns = [
    path('facilities/', SportFacilityListAPIView.as_view(), name='facility-list'),
    path('facilities/<int:pk>/', SportFacilityDetailAPIView.as_view(), name='facility-detail'),
]
