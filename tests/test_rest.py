import requests
import json
import random

host = 'localhost'
port = '9999'

def test_tsp1():
    headers = {'Content-Type': 'application/json'}
    # Known locations, known answer
    payload = {'locations': [
        {'lat': 1.23, 'lon': 76.56},
        {'lat': 25.412, 'lon': 99.485},
        {'lat': 4.333, 'lon': 12.875},
        {'lat': 94.12, 'lon': 2.112},
        {'lat': 11.815, 'lon': 78.122},
        {'lat': 33.26, 'lon': 1.026},
        {'lat': 1.306, 'lon': 45.223},
        {'lat': 17.895, 'lon': 30.256},
    ]}

    # convert dict to json by json.dumps() for body data.
    resp = requests.post(f'http://{host}:{port}/api/v0.1/solver/tsp', headers=headers,
                         data=json.dumps(payload, indent=4))

    # Validate response headers and body contents, e.g. status code.
    print (resp.content)
    assert resp.status_code == 200
    s = resp.json()

    ## We check both right response and also
    ## distance that should result
    assert 'order' in s
    assert 'total_distance' in s
    assert s['total_distance'] == 320



def test_tsp2():
    headers = {'Content-Type': 'application/json'}
    # Known locations, known answers
    payload = {'locations': [
        {'lat': 1.23, 'lon': 76.56},
        {'lat': 4.333, 'lon': 12.875},
        {'lat': 94.12, 'lon': 2.112},
        {'lat': 33.26, 'lon': 1.026},
    ]}

    # convert dict to json by json.dumps() for body data.
    resp = requests.post(f'http://{host}:{port}/api/v0.1/solver/tsp', headers=headers,
                         data=json.dumps(payload, indent=4))

    # Validate response headers and body contents, e.g. status code.
    assert resp.status_code == 200
    s = resp.json()

    ## We check both right response and also
    ## distance that should result
    assert 'order' in s
    assert 'total_distance' in s
    assert s['total_distance'] == 273



def test_tsp3():
    headers = {'Content-Type': 'application/json'}
    # Generate random locations
    locations = [{'lat': random.random()*100, 'lon': random.random()*100} for n in range(random.randint(3,20))]

    payload = {'locations': locations}

    # convert dict to json by json.dumps() for body data.
    resp = requests.post(f'http://{host}:{port}/api/v0.1/solver/tsp', headers=headers,
                         data=json.dumps(payload, indent=4))

    # Validate response headers and body contents, e.g. status code.
    assert resp.status_code == 200
    s = resp.json()

    ## we just check the right format of response
    ## we don't know what distance will be
    assert 'order' in s
    assert 'total_distance' in s

