from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import SportFacility, Category, Tag
from .serializers import SportFacilityListSerializer, SportFacilityDetailSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

class SportFacilityListAPIView(APIView):
    pagination_class = StandardResultsSetPagination

    def get(self, request, *args, **kwargs):
        queryset = SportFacility.objects.filter(is_active=True).select_related(
            'category', 'city', 'city__province'
        ).prefetch_related(
            'tags', 'images' # Prefetch images for cover image optimization
        ).order_by('name') # Default ordering

        # Filtering
        category_id = request.query_params.get('category')
        city_id = request.query_params.get('city')
        province_id = request.query_params.get('province')
        tags_param = request.query_params.getlist('tags') # Get list of tag IDs or slugs
        gender_type = request.query_params.get('gender_type')

        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if city_id:
            queryset = queryset.filter(city_id=city_id)
        if province_id:
            queryset = queryset.filter(city__province_id=province_id)
        if tags_param:
            # Assuming tags_param contains tag IDs. Use 'slug__in' if slugs are passed.
            queryset = queryset.filter(tags__id__in=tags_param).distinct()
        if gender_type in [choice[0] for choice in SportFacility.GENDER_CHOICES]:
            queryset = queryset.filter(Q(gender_type=gender_type) | Q(gender_type='B')) # Filter by specific gender or 'Both'

        # Searching
        search_query = request.query_params.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(address__icontains=search_query)
            )

        # Pagination
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request, view=self)
        serializer = SportFacilityListSerializer(paginated_queryset, many=True, context={'request': request})

        return paginator.get_paginated_response(serializer.data)

class SportFacilityDetailAPIView(APIView):
    def get(self, request, pk, *args, **kwargs):
        facility = get_object_or_404(
            SportFacility.objects.prefetch_related(
                'images', 'features', 'drawbacks', 'optional_services', 'tags'
            ).select_related('category', 'city', 'city__province'),
            pk=pk, is_active=True # Optionally restrict to active facilities
        )
        serializer = SportFacilityDetailSerializer(facility, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
