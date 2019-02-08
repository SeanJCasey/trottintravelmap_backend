from django.conf import settings
from django.db import models


class Continent(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=2, blank=True, null=True, help_text="ISO 3166-2")
    continent = models.CharField(max_length=50)
    area = models.FloatField()

    def __unicode__(self):
        return self.name


class Place(models.Model):
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=50, blank=True, null=True, help_text="Coded keyword to map to the SVG")
    region = models.CharField(max_length=50)
    area = models.FloatField(blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    continent = models.ForeignKey(Continent, on_delete=models.SET_NULL, null=True, blank=True)

    def __unicode__(self):
        return self.name


class PlaceMap(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    places = models.ManyToManyField(Place)

    @property
    def continent_count(self):
        return len(set(self.places.values_list('continent', flat=True)))

    @property
    def place_count(self):
        return self.places.count()

    @property
    def place_percent(self):
        return round(self.un_country_count / Country.objects.all().count() * 100)

    @property
    def region_count(self):
        return len(set(self.places.values_list('region', flat=True)))

    @property
    def un_country_count(self):
        return len(set(self.places.values_list('country', flat=True)))

    @property
    def un_country_area_percent(self):
        from django.db.models import Sum
        area_user = self.places.aggregate(Sum('area'))['area__sum']
        area_total = Place.objects.all().aggregate(Sum('area'))['area__sum']
        area_percent = 0
        if area_user and area_total:
            area_percent = area_user / area_total * 100
        return round(area_percent)

    def __unicode__(self):
        return "<PlaceMap for %s>" % self.user
