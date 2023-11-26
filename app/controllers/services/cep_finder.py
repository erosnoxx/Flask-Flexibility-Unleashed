import googlemaps, os, requests
from flask import jsonify
from dotenv import load_dotenv

load_dotenv()

def get_cep_google(cep):
    gmaps = googlemaps.Client(key=os.getenv('GOOGLE_API_KEY'))
    geocode_result = gmaps.geocode(cep)

    if not geocode_result:
        return None

    location_info = {}
    location_info['latitude'] = geocode_result[0]['geometry']['location']['lat']
    location_info['longitude'] = geocode_result[0]['geometry']['location']['lng']

    return location_info


def get_cep(cep):
    url = f'https://viacep.com.br/ws/{cep}/json/'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            address = data.get('logradouro', '') + ', ' + data.get('complemento', '') + ', ' + data.get('bairro', '')
            city = data.get('localidade', '')
            state = data.get('uf', '')
            google_info = get_cep_google(cep)
            if google_info != None:
                return {
                    'address': address if address != ', , ' else '',
                    'city': city,
                    'state': state,
                    'zipcode': cep,
                    'latitude': google_info['latitude'],
                    'longitude': google_info['longitude']
                }
            else:
                return {
                    'error': "CEP not found",
                    'status_code': '404'
                }
        else:
            return {
                'error': "CEP not found",
                'status_code': response.status_code
            }

    except requests.RequestException as e:
        return {'message': e, 'statuscode': '500'}


if __name__ == '__main__':
    print(get_cep('45230000'))