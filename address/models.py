from django.db import models
import uuid


class Province(models.Model):
    name = models.CharField(max_length=60, null=False)
    slug = models.CharField(max_length=60)
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=60, null=False)
    slug = models.CharField(max_length=60)
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    province = models.ForeignKey(Province, on_delete=models.PROTECT)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)


    def __str__(self):
        return self.name


class Address (models.Model):
    address = models.CharField(verbose_name='Address Field', max_length=100, null=False)
    province = models.ForeignKey(Province, on_delete=models.PROTECT, null=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT, null=True)
    phone = models.CharField(
        'phone number', max_length=11,
        null=False, blank=False,

    )
    zipcode = models.CharField(
        'zip code', max_length=12,
        null=True, blank=True,
    )

