import pytest
import math
import json

DRIVER_AMOUNT = 19

abr_cases = ['BHS', 'MES', 'VBM']


@pytest.mark.parametrize('abr', abr_cases)
def test_json_api_report(client, abr):
    response = client.get('/api/v1/report/')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    data = json.loads(response.data)
    assert len(data) == DRIVER_AMOUNT
    assert abr in data


name_cases = ['Brendon Hartley', 'Marcus Ericsson', 'Valtteri Bottas']


@pytest.mark.parametrize('name', name_cases)
def test_json_api_drivers(client, name):
    response = client.get('/api/v1/report/drivers/')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    data = json.loads(response.data)
    assert len(data) == DRIVER_AMOUNT
    assert name in data


json_driver_test_case = [
    ('SVF', 'Sebastian Vettel', 1, 64.415),
    ('FAM', 'Fernando Alonso', 5, 72.657),
    ('CSR', 'Carlos Sainz', 10, 72.95),
    ('KMH', 'Kevin Magnussen', 15, 73.393),
    ('LHM', 'Lewis Hamilton', 19, -407.54)
]


@pytest.mark.parametrize('abr, name, position, lap_time', json_driver_test_case)
def test_json_api_driver(client, abr, name, position, lap_time):
    response = client.get(f'/api/v1/report/drivers/{abr}/')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    data = json.loads(response.data)
    assert name in data
    assert data[name]['position'] == position
    assert math.isclose(data[name]['lap_time'], lap_time, rel_tol=1e-9)
