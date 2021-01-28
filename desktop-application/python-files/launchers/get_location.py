import json
import geocoder

def get_location():
    g = geocoder.ip('me')
    location_lat_long = g.latlng
    return location_lat_long

