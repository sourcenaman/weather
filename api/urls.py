from django.urls import path
from .views import *


urlpatterns = [
    path('duration/', duration_data, name='duration_data'),
    path('season/', season_data, name='season_data'),
]

