# This is a set of samples for use with Azure Maps.
# This code covers creating a geofence, then querying it.
# The three queries are for inside the geofence, outside, then inside but near the edge
#
# To use this code, create a .env file with an entry called MAPS_KEY set to the primary 
# or secondary key of your Azure Maps resource.
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
geofence_udid = ''

def upload_geofence():
    global geofence_udid
    geofence_upload_url = 'https://atlas.microsoft.com/mapData/upload'
    params={
        'subscription-key': maps_key,
        'api-version': '1.0',
        'dataFormat': 'geojson'
    }

    with open('geofence.json') as json_file:
        data = json.load(json_file)

        geofence_create_response = requests.post(geofence_upload_url, 
                                                 params=params, 
                                                 json=data)
        geofence_location = geofence_create_response.headers['location']

        response = requests.get(geofence_location, params=params)
        response_json = response.json()

        while 'status' in response_json and response_json['status'] == 'Running':
            time.sleep(0.5)
            response = requests.get(geofence_location, params=params)
            response_json = response.json()
        
        resource_location = response.json()['resourceLocation']
        response = requests.get(resource_location, params=params)

        geofence_udid = response.json()['udid']
        print()
        print('Geofence UDID:', geofence_udid)
        print()

def check_geofence(lat, lon):
    check_geofence_url = 'https://atlas.microsoft.com/spatial/geofence/json'
    params={
        'subscription-key': maps_key,
        'api-version': '1.0',
        'udid': geofence_udid,
        'lat': lat,
        'lon': lon,
        'deviceId': 'device',
        'searchBuffer': 50
    }

    check_geofence_response = requests.get(check_geofence_url, params=params)
    response_json = check_geofence_response.json()
    print()
    print('Distance to geofence:', response_json['geometries'][0]['distance'])
    print('Nearest geofence location', response_json['geometries'][0]['nearestLon'], 
          ',', response_json['geometries'][0]['nearestLat'])
    print()

def check_geofence_middle():
    print()
    print('Checking a point inside the geofence')
    check_geofence(47.661976221969933, -122.124838829040525)

def check_geofence_outside():
    print()
    print('Checking a point outside the geofence')
    check_geofence(48, -122)

def check_geofence_edge():
    print()
    print('Checking a point on the edge of the geofence')
    check_geofence(47.654, -122.147)


upload_geofence()
check_geofence_middle()
check_geofence_outside()
check_geofence_edge()