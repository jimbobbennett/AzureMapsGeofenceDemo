# Azure Maps Geofence Demo

This is demo code showing how to use Azure Maps geofences to test if a point is inside a geofence, and get alerts when a device crosses a geofence.

## Getting started

To create an Azure Maps resource, first you need an Azure account.

* Sign up for free and get $200 of credit to use for 30 days and 12 months of free services
  [aka.ms/FreeAZ](https://aka.ms/FreeAZ)

* If you are a student, you can get $100 of credit and free services that last a year,
  and can be renewed each year you are a student, and doesn't require a credit card:
  [aka.ms/FreeStudentAzure](https://aka.ms/FreeStudentAzure)

Once you have an account, you will need to create an Azure Maps resource.

After your resource is created you will need to configure this code to use it

* Head to the *Authentication* tab of your Azure Maps resource in the Azure Portal and copy the value of the primary or secondary key
* Create a file called `.env`
* Add the following code to this file:

  ```sh
  MAPS_KEY=<key>
  ```

  Set the value of `<key>` to be the primary or secondary key of your maps resource.

## Running the code

Before you can run this code, you will need to install some pip packages:

```sh
pip3 install -r requirements.txt
```

### GeoFenceSamples.py

This Python file contains code to create a geofence, then query it using 3 different sets of coordinates.

#### `upload_geofence`

This function loads a geofence as [GeoJSON](http://geojson.org/), then uploads it to Azure Maps:

* The geofence is loaded from the `geofence.json` file. This data was created by drawing a rectangular geofence using [geojson.io](http://geojson.io/).
* This data is sent as a POST request to the Azure Maps data REST API, using the map key to authenticate the call.
* Once posted, the response contains a header with a `location` value.
* A GET request is made to this `location` to get the UDID of the geofence - it's unique id.

#### `check_geofence`

This function checks a given point against the geofence

* A call is made to the geofence REST API, passing in a latitude and longitude as well as the UDID of the geofence
* The results come back as JSON giving the distance to the nearest point on the geofence, as well as the location of the nearest point
  * A negative distance is inside the geofence, positive is outside.
  * The value is either 999, -999 or a distance from -50 to 50.
    * 999 means outside the geofence
    * -999 means inside the geofence
    * A value from -50 to 50 means the point is near the geofence, with the value showing the distance. This is because GPS receivers are not accurate, so a value just inside the geofence could come from a receiver just outside. The 50 is a range of 50 meters, and this can be configured in the call.
* The distance and location is printed to the console

#### `check_geofence_middle`

This function checks a point in the middle of the geofence against the geofence.

#### `check_geofence_outside`

This function checks a point outside of the geofence against the geofence.

#### `check_geofence_edge`

This function checks a point close to the edge of the geofence against the geofence.

### TriggerGeofenceEnter.py

This python file contains code to run geofence queries from outside, then inside the geofence. To use this file:

* Run the code in `GeoFenceSamples.py`, and copy the geofence UDUD
* Add a new entry to the `.env` file:

  ```sh
  GEOFENCE_UDID=<udid>
  ```

  and set `<udid>` to be the value of the geofence UDID.

* Load your Azure Maps resource in the Azure Portal.

* Open the *Events* tab

* Add a new event subscribing to the **Geofence Entered** event, make it do whatever you want (for example use a web hook to call a logic app).

Run this code. It will call the same REST API to check the geofence, except with some new parameters:

```sh
'mode': 'EnterAndExit',
'isAsync': 'True'
```

This tell Azure Maps to trigger geofence events. The first two calls are outside the geofence, the third call is inside. Triggering them all in order will cause the maps to detect that the geofence has been entered and fire the event.

Azure maps tracks these entries by a device id. This is set on the geofence call, so if a call with the same device id happens outside the geofence, then inside, it knows that the device has entered the geofence.