import requests, json, os, time

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

        geofence_create_response = requests.post(geofence_upload_url, params=params, json=data)
        geofence_location = geofence_create_response.headers['location']

        response = requests.get(geofence_location, params=params)
        response_json = response.json()

        while 'status' in response_json and response_json['status'] == 'InProgress':
            time.sleep(0.5)
            response = requests.get(geofence_location, params=params)
            response_json = response.json()

        geofence_udid = response.json()['udid']
        print()
        print('Geofence UDID:', geofence_udid)
        print()

def download_map_tile():
    map_tile_download_url = 'https://atlas.microsoft.com/map/static/png'
    params={
        'subscription-key': maps_key,
        'api-version': '1.0',
        'layer': 'basic',
        'style': 'main',
        'center': '-122.124838829040525,47.661976221969933',
        'zoom': 9,
        'path': '||-122.41864 47.54548|-122.41864 47.70502|-122.00867 47.70502|-122.00867 47.54548|-122.41864 47.54548'
    }

    map_tile_response = requests.get(map_tile_download_url, params=params)
    with open("map_tile.png", "wb") as map_file:
        map_file.write(map_tile_response.content)

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
    print('Nearest geofence location', response_json['geometries'][0]['nearestLon'], ',', response_json['geometries'][0]['nearestLat'])
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
download_map_tile()
check_geofence_middle()
check_geofence_outside()
check_geofence_edge()