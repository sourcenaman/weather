from .models import *
from rest_framework.serializers import *
import calendar


class InstrumentResource(ModelSerializer):
    class Meta:
        model = Instrument
        exclude = ('id', )

class DataSerializer(ModelSerializer):
    month = SerializerMethodField()
    instrument = InstrumentResource()
    class Meta:
        model = Data
        fields = ('year', 'month', 'data', 'instrument')
        depth = 1  
    #get month name based on month number
    def get_month(self, instance):
        month = instance.month
        return calendar.month_name[month]

class SeasonalDataSerializer(ModelSerializer):
    instrument = InstrumentResource()
    season = SerializerMethodField()
    class Meta:
        model = SeasonalData
        fields = ('year', 'season', 'data', 'instrument')
        depth = 1
    #get full season name
    def get_season(self, instance):
        season = instance.season.verbose
        return season

#for validation of /duration/ request body
class DataValidateSerializer(Serializer):
    CHOICES = (
        ("Ranked", "ranked"),
        ("Date", "date"),
        ("ranked", "ranked"),
        ("date", "date"),
    )
    year = ListField(required=True, child=IntegerField(min_value=1800, max_value=2021))
    month = ListField(required=True, child=IntegerField(min_value=1, max_value=12))
    parameters = ListField(required=True, child=CharField(max_length=15))
    region = ListField(required=True, child=CharField(max_length=20))
    type = ChoiceField(choices=CHOICES, required=True)

#for validation of /season/ request body
class SeasonalDataValidateSerializer(Serializer):
    CHOICES_TYPE = (
        ("Ranked", "ranked"),
        ("Date", "date"),
        ("ranked", "ranked"),
        ("date", "date"),
    )

    CHOICES_SEASON = (
        ("Winter", "winter"),
        ("Summer", "summer"),
        ("Spring", "spring"),
        ("Autumn", "autumn"),
        ("Annual", "annual"),
    )
    year = ListField(required=True, child=IntegerField(min_value=1800, max_value=2021))
    season = MultipleChoiceField(choices=CHOICES_SEASON, required=True)
    parameters = ListField(required=True, child=CharField(max_length=15))
    region = ListField(required=True, child=CharField(max_length=20))
    type = ChoiceField(choices=CHOICES_TYPE, required=True)

