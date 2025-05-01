from django.shortcuts import render
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Province, City
from .serializers import ProvinceSerializer, CitySerializer

# Create your views here.

class ProvinceListAPIView(generics.ListAPIView):
    """
    API endpoint for listing and searching Provinces.
    Supports searching on the 'name' field using the 'search' query parameter.
    """
    queryset = Province.objects.all().order_by('name')
    serializer_class = ProvinceSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    pagination_class = None # Or your preferred pagination class


class CityListAPIView(generics.ListAPIView):
    """
    API endpoint for listing Cities.
    Supports filtering by 'province' ID and searching on the 'name' field.
    Use query parameters: ?province=<province_id>&search=<city_name>
    """
    queryset = City.objects.select_related('province').order_by('name')
    serializer_class = CitySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['province'] # Filter by province ID
    search_fields = ['name'] # Search by city name
    pagination_class = None # Or your preferred pagination class
