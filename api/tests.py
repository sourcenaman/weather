import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from .models import *
from .serializers import *


# initialize the APIClient app
client = Client()

#Test to get all the data from duration_data view
class GetAllDataTest(TestCase):
    #insert data in temporary database
    def setUp(self):
        instrument1 = Instrument.objects.create(parameters="Tmax", region="UK", unit="Celsius")
        Data.objects.create(year=1800, month=1, data=19.7, instrument=instrument1)
        instrument2 = Instrument.objects.create(parameters="Tmin", region="England", unit="Celsius")
        Data.objects.create(year=1800, month=1, data=1.7, instrument=instrument2)
        instrument3 = Instrument.objects.create(parameters="Sunshine", region="UK", unit="Days")
        Data.objects.create(year=2020, month=4, data=10, instrument=instrument3)
        instrument4 = Instrument.objects.create(parameters="RainFall", region="Wales", unit="mm")
        Data.objects.create(year=1920, month=10, data=3, instrument=instrument4)
        instrument5 = Instrument.objects.create(parameters="Tmean", region="England", unit="Celsius")
        Data.objects.create(year=1976, month=12, data=20, instrument=instrument5)

        self.payload_ranked = {
            "year": [],
            "month": [],
            "parameters": [],
            "region": [],
            "type": "ranked"
        }

        self.payload_date = {
            "year": [],
            "month": [],
            "parameters": [],
            "region": [],
            "type": "date"
        }

    def test_duration_data(self):
        #get api response for ranked data
        response_ranked = client.post(
            reverse("duration_data"),
            data=json.dumps(self.payload_ranked),
            content_type="application/json"
            )
        data_ranked = Data.objects.all().order_by('month', '-data')
        #get serializer response for ranked data
        serializer_ranked = DataSerializer(data_ranked, many=True)
        self.assertEqual(response_ranked.data, serializer_ranked.data)
        #get api response for date data
        response_date = client.post(
            reverse("duration_data"),
            data=json.dumps(self.payload_date),
            content_type="application/json"
            )
        data_date = Data.objects.all().order_by('year')
        #get serializer response for date data
        serializer_date = DataSerializer(data_date, many=True)
        self.assertEqual(response_date.data, serializer_date.data)

#Test to get all the data from season_data view
class GetAllSeasonalDataTest(TestCase):
    #insert data in temporary database
    def setUp(self):
        instrument1 = Instrument.objects.create(parameters="Tmax", region="UK", unit="Celsius")
        seasons1 = Seasons.objects.create(name="win", verbose="Winter")
        SeasonalData.objects.create(year=1800, data=19.7, instrument=instrument1, season=seasons1)
        instrument2 = Instrument.objects.create(parameters="Tmin", region="England", unit="Celsius")
        seasons2 = Seasons.objects.create(name="sum", verbose="Summer")
        SeasonalData.objects.create(year=1800, data=1.7, instrument=instrument2, season=seasons2)
        instrument3 = Instrument.objects.create(parameters="Sunshine", region="UK", unit="Days")
        seasons3 = Seasons.objects.create(name="aut", verbose="Autumn")
        SeasonalData.objects.create(year=2020, data=10, instrument=instrument3, season=seasons3)
        instrument4 = Instrument.objects.create(parameters="RainFall", region="Wales", unit="mm")
        seasons4 = Seasons.objects.create(name="spr", verbose="Spring")
        SeasonalData.objects.create(year=1920, data=3, instrument=instrument4, season=seasons4)
        instrument5 = Instrument.objects.create(parameters="Tmean", region="England", unit="Celsius")
        seasons5 = Seasons.objects.create(name="ann", verbose="Annual")
        SeasonalData.objects.create(year=1976, data=20, instrument=instrument5, season=seasons5)

        self.payload_ranked = {
            "year": [],
            "season": [],
            "parameters": [],
            "region": [],
            "type": "ranked"
        }

        self.payload_date = {
            "year": [],
            "season": [],
            "parameters": [],
            "region": [],
            "type": "date"
        }

    def test_season_data(self):
        #get api response for ranked data
        response_ranked = client.post(
            reverse("season_data"),
            data=json.dumps(self.payload_ranked),
            content_type="application/json"
            )
        data_ranked = SeasonalData.objects.all().order_by('year', '-data')
        #get serializer response for ranked data
        serializer_ranked = SeasonalDataSerializer(data_ranked, many=True)
        self.assertEqual(response_ranked.data, serializer_ranked.data)
        #get api response for date data
        response_date = client.post(
            reverse("season_data"),
            data=json.dumps(self.payload_date),
            content_type="application/json"
            )
        data_date = SeasonalData.objects.all().order_by('year')
        #get serializer response for date data
        serializer_date = SeasonalDataSerializer(data_date, many=True)
        self.assertEqual(response_date.data, serializer_date.data)

#Test to get filtered data from duration_data view
class GetDataTest(TestCase):
    #insert data in temporary database
    def setUp(self):
        instrument1 = Instrument.objects.create(parameters="Tmax", region="UK", unit="Celsius")
        Data.objects.create(year=1800, month=1, data=19.7, instrument=instrument1)
        instrument2 = Instrument.objects.create(parameters="Tmin", region="England", unit="Celsius")
        Data.objects.create(year=1800, month=1, data=1.7, instrument=instrument2)
        instrument3 = Instrument.objects.create(parameters="Sunshine", region="UK", unit="Days")
        Data.objects.create(year=2020, month=4, data=10, instrument=instrument3)
        instrument4 = Instrument.objects.create(parameters="RainFall", region="Wales", unit="mm")
        Data.objects.create(year=1920, month=10, data=3, instrument=instrument4)
        instrument5 = Instrument.objects.create(parameters="Tmean", region="England", unit="Celsius")
        Data.objects.create(year=1976, month=12, data=20, instrument=instrument5)

        self.payload_ranked_valid = {
            "year": [1920],
            "month": [10],
            "parameters": [],
            "region": [],
            "type": "ranked"
        }

        self.payload_date_valid = {
            "year": [1800],
            "month": [],
            "parameters": ["Tmin"],
            "region": [],
            "type": "date"
        }

        self.payload_ranked_invalid = {
            "year": ["Twenty Twenty"],
            "month": [],
            "parameters": [],
            "region": [],
            "type": "ranked"
        }

        self.payload_date_invalid = {
            "year": [],
            "month": ["January"],
            "parameters": [],
            "region": [],
            "type": "date"
        }

    # test for valid payload
    def test_duration_data_valid(self):
        # get api response for ranked data
        response_ranked = client.post(
            reverse("duration_data"),
            data=json.dumps(self.payload_ranked_valid),
            content_type="application/json"
            )
        self.assertEqual(response_ranked.status_code, status.HTTP_200_OK)
        #get api response for date data
        response_date = client.post(
            reverse("duration_data"),
            data=json.dumps(self.payload_date_valid),
            content_type="application/json"
            )
        self.assertEqual(response_date.status_code, status.HTTP_200_OK)

    # test for invalid payload
    def test_duration_data_invalid(self):
        # get api response for ranked data
        response_ranked = client.post(
            reverse("duration_data"),
            data=json.dumps(self.payload_ranked_invalid),
            content_type="application/json"
            )
        self.assertEqual(response_ranked.status_code, status.HTTP_400_BAD_REQUEST)
        #get api response for date data
        response_date = client.post(
            reverse("duration_data"),
            data=json.dumps(self.payload_date_invalid),
            content_type="application/json"
            )
        self.assertEqual(response_date.status_code, status.HTTP_400_BAD_REQUEST)

#Test to get filtered data from season_data view
class GetSeasonalDataTest(TestCase):
    #insert data in temporary database
    def setUp(self):
        instrument1 = Instrument.objects.create(parameters="Tmax", region="UK", unit="Celsius")
        seasons1 = Seasons.objects.create(name="win", verbose="Winter")
        SeasonalData.objects.create(year=1800, data=19.7, instrument=instrument1, season=seasons1)
        instrument2 = Instrument.objects.create(parameters="Tmin", region="England", unit="Celsius")
        seasons2 = Seasons.objects.create(name="sum", verbose="Summer")
        SeasonalData.objects.create(year=1800, data=1.7, instrument=instrument2, season=seasons2)
        instrument3 = Instrument.objects.create(parameters="Sunshine", region="UK", unit="Days")
        seasons3 = Seasons.objects.create(name="aut", verbose="Autumn")
        SeasonalData.objects.create(year=2020, data=10, instrument=instrument3, season=seasons3)
        instrument4 = Instrument.objects.create(parameters="RainFall", region="Wales", unit="mm")
        seasons4 = Seasons.objects.create(name="spr", verbose="Spring")
        SeasonalData.objects.create(year=1920, data=3, instrument=instrument4, season=seasons4)
        instrument5 = Instrument.objects.create(parameters="Tmean", region="England", unit="Celsius")
        seasons5 = Seasons.objects.create(name="ann", verbose="Annual")
        SeasonalData.objects.create(year=1976, data=20, instrument=instrument5, season=seasons5)

        self.payload_ranked_valid = {
            "year": [1920],
            "season": ["Annual"],
            "parameters": [],
            "region": [],
            "type": "ranked"
        }

        self.payload_date_valid = {
            "year": [1800],
            "season": [],
            "parameters": [],
            "region": [],
            "type": "date"
        }

        self.payload_ranked_invalid = {
            "year": ["Twenty Twenty"],
            "season": [],
            "parameters": [],
            "region": [],
            "type": "ranked"
        }

        self.payload_date_invalid = {
            "year": [],
            "month": ["January"],
            "parameters": [],
            "region": [],
            "type": "date"
        }

    # test for valid payload
    def test_season_data_valid(self):
        # get api response for ranked data
        response_ranked = client.post(
            reverse("season_data"),
            data=json.dumps(self.payload_ranked_valid),
            content_type="application/json"
            )
        self.assertEqual(response_ranked.status_code, status.HTTP_200_OK)
        #get api response for date data
        response_date = client.post(
            reverse("season_data"),
            data=json.dumps(self.payload_date_valid),
            content_type="application/json"
            )
        self.assertEqual(response_date.status_code, status.HTTP_200_OK)

    # test for invalid payload
    def test_season_data_invalid(self):
        # get api response for ranked data
        response_ranked = client.post(
            reverse("season_data"),
            data=json.dumps(self.payload_ranked_invalid),
            content_type="application/json"
            )
        self.assertEqual(response_ranked.status_code, status.HTTP_400_BAD_REQUEST)
        #get api response for date data
        response_date = client.post(
            reverse("season_data"),
            data=json.dumps(self.payload_date_invalid),
            content_type="application/json"
            )
        self.assertEqual(response_date.status_code, status.HTTP_400_BAD_REQUEST)


