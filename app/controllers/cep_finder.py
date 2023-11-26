import googlemaps
import os
from dotenv import load_dotenv

load_dotenv()


def get_address(zipcode):
    gmaps = googlemaps.Client(key=os.getenv('GOOGLE_API_KEY'))
    geocode_result = gmaps.geocode(zipcode)

    if not geocode_result:
        return None

    location = geocode_result[0]

    address_components = {
        component['types'][0]: component['long_name']
        for component in location['address_components']
    }

    address = {
        'neighborhood': geocode_result[0]['address_components'][1]['long_name'],
        'city': geocode_result[0]['address_components'][2]['long_name'],
        'state': address_components.get('administrative_area_level_1', ''),
        'country': address_components.get('country', ''),
        'cep': address_components.get('postal_code', ''),
        'latitude': location['geometry']['location']['lat'],
        'longitude': location['geometry']['location']['lng']
    }

    return address