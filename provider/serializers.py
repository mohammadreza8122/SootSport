from rest_framework import serializers
from .models import Category, Tag, SportFacility, FacilityImage, Feature, Drawback, OptionalService, TimeSlot
# Import actual models from address app
from address.models import City, Province
from django.utils.translation import gettext_lazy as _
from django.db.models import Min, Max
from decimal import Decimal
import datetime

# Actual serializers based on address.models
class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['id', 'name', 'slug'] # Adjust fields as needed

class CitySerializer(serializers.ModelSerializer):
    # province = ProvinceSerializer(read_only=True) # Keep nested or just show ID/name
    province_name = serializers.CharField(source='province.name', read_only=True)
    class Meta:
        model = City
        fields = ['id', 'name', 'slug', 'province', 'province_name'] # Adjust fields as needed
        extra_kwargs = {
            'province': {'write_only': True} # Only need ID for writing/filtering
        }


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']

class FacilityImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityImage
        fields = ['id', 'image', 'caption', 'is_cover']

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['id', 'text']

class DrawbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drawback
        fields = ['id', 'text']

class OptionalServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionalService
        fields = ['id', 'name', 'price', 'description']

class TimeSlotSerializer(serializers.ModelSerializer):
    final_price = serializers.SerializerMethodField()
    is_reserved = serializers.SerializerMethodField() # Example: Check if slot is already reserved

    class Meta:
        model = TimeSlot
        fields = [
            'id', 'date', 'start_time', 'end_time', 'base_price',
            'discount', 'is_available', 'gender_type', 'final_price', 'is_reserved'
        ]
        read_only_fields = ['final_price', 'is_reserved']

    def get_final_price(self, obj):
        # Use the model method, ensure it returns a serializable type (like Decimal or float)
        return obj.get_final_price()

    def get_is_reserved(self, obj):
        # Simple check if any reservation exists for this slot
        # In a real app, you might need more complex logic based on reservation status
        return obj.reservations.exists() # Assumes Reservation model has related_name='reservations'


class SportFacilityListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    city = CitySerializer(read_only=True) # Use the actual CitySerializer
    # province = ProvinceSerializer(read_only=True) # Province info is likely in CitySerializer
    cover_image = serializers.SerializerMethodField()
    price_range = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True) # Add tags to list view

    class Meta:
        model = SportFacility
        fields = [
            'id', 'name', 'city', 'category', 'tags', # Removed province as it's in city
            'gender_type', 'is_active', 'cover_image', 'price_range'
        ]

    def get_cover_image(self, obj):
        cover = obj.images.filter(is_cover=True).first()
        if cover:
            request = self.context.get('request')
            return request.build_absolute_uri(cover.image.url) if request else cover.image.url
        # Optionally return a default image URL
        return None

    def get_price_range(self, obj):
        # Get price range from available future time slots
        today = datetime.date.today()
        price_agg = obj.time_slots.filter(is_available=True, date__gte=today).aggregate(
            min_price=Min('base_price'),
            max_price=Max('base_price')
        )
        min_p = price_agg.get('min_price')
        max_p = price_agg.get('max_price')

        if min_p is not None and max_p is not None:
            # Here you might want to apply discounts as well for a more accurate range
            # For simplicity, using base_price range.
            if min_p == max_p:
                 return f"{min_p:,.0f}" # Format without decimals
            return f"{min_p:,.0f} - {max_p:,.0f}" # Format without decimals
        return _("نامشخص")


class SportFacilityDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    city = CitySerializer(read_only=True) # Use the actual CitySerializer
    # province = ProvinceSerializer(read_only=True) # Province info is likely in CitySerializer
    images = FacilityImageSerializer(many=True, read_only=True)
    features = FeatureSerializer(many=True, read_only=True)
    drawbacks = DrawbackSerializer(many=True, read_only=True)
    optional_services = OptionalServiceSerializer(many=True, read_only=True)
    # Optionally include available time slots directly, or provide a separate endpoint
    # available_time_slots = TimeSlotSerializer(many=True, read_only=True, source='get_available_slots') # Example

    class Meta:
        model = SportFacility
        fields = [
            'id', 'name', 'description', 'address', 'city', # Removed province
            'category', 'tags', 'gender_type', 'is_active',
            'images', 'features', 'drawbacks', 'optional_services',
            'created_at', 'updated_at'
            # 'available_time_slots' # Add if you include slots here
        ]

    # Example method if you want to filter slots in the serializer
    # def get_available_slots(self, obj):
    #     today = datetime.date.today()
    #     return obj.time_slots.filter(is_available=True, date__gte=today).order_by('date', 'start_time') 