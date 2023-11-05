import pytest
import math
import json

from app.app import API_REPORT_ROUTE, API_DRIVERS_ROUTE

DRIVER_AMOUNT = 19

abbr_cases = ['BHS', 'MES', 'VBM']


@pytest.mark.parametrize('abbr', abbr_cases)
def test_json_api_report(client, abbr):
    response = client.get(API_REPORT_ROUTE)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    data = json.loads(response.data)
    assert len(data) == DRIVER_AMOUNT
    assert abbr in data


name_cases = ['Brendon Hartley', 'Marcus Ericsson', 'Valtteri Bottas']


@pytest.mark.parametrize('name', name_cases)
def test_json_api_drivers(client, name):
    response = client.get(API_DRIVERS_ROUTE)
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


@pytest.mark.parametrize(
    'abbr, name, position, lap_time', json_driver_test_case)
def test_json_api_driver(client, abbr, name, position, lap_time):
    response = client.get(f'{API_DRIVERS_ROUTE}/{abbr}')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    data = json.loads(response.data)
    assert name in data
    assert data[name]['position'] == position
    assert math.isclose(data[name]['lap_time'], lap_time, rel_tol=1e-9)
