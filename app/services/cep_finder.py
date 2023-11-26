import requests
url = 'https://viacep.com.br/ws/'

def get_cep(cep):
    r = requests.get(url + cep + '/json/')
    return r.json()