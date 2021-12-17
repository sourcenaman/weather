from django.db import models

# Create your models here.
class Instrument(models.Model):
    parameters = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    unit = models.CharField(max_length=10)


class Data(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    instrument = models.ForeignKey(Instrument, related_name='month_instrument', on_delete=models.CASCADE)
    data = models.FloatField(blank=True, null=True)


class Seasons(models.Model):
    name = models.CharField(max_length=10)
    verbose = models.CharField(max_length=50)


class SeasonalData(models.Model):
    year = models.IntegerField()
    instrument = models.ForeignKey(Instrument, related_name='season_instrument', on_delete=models.CASCADE)
    data = models.FloatField(blank=True, null=True)
    season = models.ForeignKey(Seasons, related_name='season', on_delete=models.CASCADE)


