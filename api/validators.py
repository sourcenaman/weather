from .serializers import *

def validate_data(request):
    res = {}
    res["success"] = True
    res["errors"] = None
    res["details"] = None
    validation = DataValidateSerializer(data=request)
    if validation.is_valid():
        res["success"] = True
    else:
        res["success"] = False
        res["details"] = "Bad Request Body"
        res["errors"] = validation.errors
    return res

def validate_seasonal_data(request):
    res = {}
    res["success"] = True
    res["errors"] = None
    res["details"] = None
    validation = SeasonalDataValidateSerializer(data=request)
    if validation.is_valid():
        res["success"] = True
    else:
        res["success"] = False
        res["details"] = "Bad Request Body"
        res["errors"] = validation.errors
    return res


