import pytest

from xml.etree import ElementTree

from app.app import API_REPORT_ROUTE, API_DRIVERS_ROUTE

DRIVER_AMOUNT = 19

xml_api_test_case = [(0, 'BHS'), (9, 'LSW'), (18, 'VBM')]


@pytest.mark.parametrize('position, abbr', xml_api_test_case)
def test_xml_api_report(client, position, abbr):
    response = client.get(API_REPORT_ROUTE, query_string={'format': 'xml'})
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/xml'

    root = ElementTree.fromstring(response.data)
    assert root.tag == 'report'
    assert len(root) == DRIVER_AMOUNT
    abbr_elements = root.findall('abbr')
    assert abbr_elements[position].text == abbr


xml_api_drivers_case = [
    (0, 'Sebastian Vettel'),
    (9, 'Carlos Sainz'),
    (18, 'Lewis Hamilton'),
]


@pytest.mark.parametrize('position, name', xml_api_drivers_case)
def test_xml_api_drivers(client, position, name):
    response = client.get(API_DRIVERS_ROUTE, query_string={'format': 'xml'})
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/xml'

    main = ElementTree.fromstring(response.data)
    assert main.tag == 'drivers'
    assert len(main) == DRIVER_AMOUNT
    driver_elements = main.findall('driver')
    assert driver_elements[position].text == name


xml_driver_test_case = [
    ('SVF', 'Sebastian Vettel', '1', '64.415'),
    ('FAM', 'Fernando Alonso', '5', '72.657'),
    ('CSR', 'Carlos Sainz', '10', '72.95'),
    ('KMH', 'Kevin Magnussen', '15', '73.393'),
    ('LHM', 'Lewis Hamilton', '19', '-407.54'),
]


@pytest.mark.parametrize('abbr, name, position, lap_time', xml_driver_test_case)
def test_xml_api_driver(client, abbr, name, position, lap_time):
    response = client.get(
        f'{API_DRIVERS_ROUTE}/{abbr}', query_string={'format': 'xml'}
    )
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/xml'

    root = ElementTree.fromstring(response.data)
    assert root.tag == 'driver'
    assert root.text == name
    assert root.find('position').text == position
    assert root.find('lap_time').text == lap_time
