from django.http.response import HttpResponse
from .serializers import *
from .models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .validators import *



'''
    request = {
        "year": [2021, 2020], If empty then it will include all the years.
        "month": [], If empty then it will include all the months
        "parameters": [], If empty then it will include all the parameters
        "region": [], If empty then it will include all the regions
        "type": "ranked" Choice field ["ranked", "Ranked", "date", "Date"]
    }
    response = {
        "year": 2020,
        "month": "January",
        "data": 259.7,
        "instrument": {
            "parameters": "Rainfall",
            "region": "Scotland_N",
            "unit": "mm"
        }
    }
'''
@api_view(['POST'])
def duration_data(request):
    data = request.data
    res = validate_data(data)
    if res["success"] == False:
        return Response(res, status=status.HTTP_400_BAD_REQUEST)
    new_data = {
        "year__in": data['year'] if data['year'] else Data.objects.distinct().values_list('year'),
        "month__in": data['month'] if data['month'] else Data.objects.distinct().values_list('month'),
        "instrument__parameters__in": data['parameters'] if data['parameters'] else Instrument.objects.distinct().values_list('parameters'),
        "instrument__region__in": data['region'] if data['region'] else Instrument.objects.distinct().values_list('region')
    }
    if data["type"].lower() == "ranked":
        query_set = Data.objects.filter(**new_data).order_by('month', '-data')
    elif data["type"].lower() == "date":
        query_set = Data.objects.filter(**new_data).order_by('year')
    serializer_class = DataSerializer(query_set, many=True)
    return Response(serializer_class.data)

'''
    request = {
        "year": [2021, 2020], If empty then it will include all the years.
        "season": [], If empty then it will include all the seasons
        "parameters": [], If empty then it will include all the parameters
        "region": [], If empty then it will include all the regions
        "type": "ranked" Choice field ["ranked", "Ranked", "date", "Date"]
    }
    response = {
        "year": 2020,
        "season": "Winter",
        "data": 377.0,
        "instrument": {
            "parameters": "Rainfall",
            "region": "England_N",
            "unit": "mm"
        }
    }
'''
@api_view(['POST'])
def season_data(request):
    data = request.data
    res = validate_seasonal_data(data)
    if res["success"] == False:
        return Response(res, status=status.HTTP_400_BAD_REQUEST)
    new_data = {
        "year__in": data['year'] if data['year'] else SeasonalData.objects.distinct().values_list('year'),
        "season__verbose__in": data['season'] if data['season'] else Seasons.objects.distinct().values_list('verbose'),
        "instrument__parameters__in": data['parameters'] if data['parameters'] else Instrument.objects.distinct().values_list('parameters'),
        "instrument__region__in": data['region'] if data['region'] else Instrument.objects.distinct().values_list('region')
    }
    if data["type"].lower() == "ranked":
        query_set = SeasonalData.objects.filter(**new_data).order_by('year', '-data')
    elif data["type"].lower() == "date":
        query_set = SeasonalData.objects.filter(**new_data).order_by('year')
    serializer_class = SeasonalDataSerializer(query_set, many=True)
    return Response(serializer_class.data)

