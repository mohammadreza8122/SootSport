from rest_framework import serializers
from .models import Province, City

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['id', 'name', 'slug', 'uuid'] # uuid هم اضافه شد

class CitySerializer(serializers.ModelSerializer):
    province_name = serializers.CharField(source='province.name', read_only=True)

    class Meta:
        model = City
        fields = ['id', 'name', 'slug', 'province', 'province_name', 'uuid'] # uuid هم اضافه شد
        extra_kwargs = {
            'province': {'write_only': True} # فقط برای فیلتر کردن نیاز است
        } 