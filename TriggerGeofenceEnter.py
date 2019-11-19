# This is a set of samples for use with Azure Maps events.
# This code covers querying an existing geofence to trigger an event.
# You will need to add an event handler to you Azure Maps resource.
#
# To use this code, create a .env file with two entries:
# MAPS_KEY set to the primary or secondary key of your Azure Maps resource.
# GEOFENCE_UDID set to the UDID of a geofence created using the GeoFenceSamples.py file
# 
# To create an Azure Maps resource, first you need an Azure account.
#
# * Sign up for free and get $200 of credit to use for 30 days and 12 months of free services
#   https://aka.ms/FreeAZ
# 
# * If you are a student, you can get $100 of credit and free services that last a year,
#   and can be renewed each year you are a student, and doesn't require a credit card:
#   https://aka.ms/FreeStudentAzure
#
# All the docs for this are here: https://aka.ms/AzMapsGeofence

import requests, json, os, time
from dotenv import load_dotenv

load_dotenv()

maps_key = os.environ['MAPS_KEY']
geofence_udid = os.environ['GEOFENCE_UDID']

def check_geofence(lat, lon):
    check_geofence_url = 'https://atlas.microsoft.com/spatial/geofence/json'
    params={
        'subscription-key': maps_key,
        'api-version': '1.0',
        'udid': geofence_udid,
        'lat': lat,
        'lon': lon,
        'deviceId': 'device',
        'searchBuffer': 50,
        'mode': 'EnterAndExit',
        'isAsync': 'True'
    }

    check_geofence_response = requests.get(check_geofence_url, params=params)
    response_json = check_geofence_response.json()
    print()
    print('Event published:', response_json['isEventPublished'])
    print('Distance to geofence:', response_json['geometries'][0]['distance'])
    print('Nearest geofence location', response_json['geometries'][0]['nearestLon'], ',', response_json['geometries'][0]['nearestLat'])
    print()

check_geofence(49, -122)
check_geofence(48, -122)
check_geofence(47.661976221969933, -122.124838829040525)
