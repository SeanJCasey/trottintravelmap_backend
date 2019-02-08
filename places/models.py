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
