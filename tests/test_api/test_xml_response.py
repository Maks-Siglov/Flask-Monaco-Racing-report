import pytest

from xml.etree import ElementTree

DRIVER_AMOUNT = 19
API_XML_REPORT_ROUT = '/api/v1/report/?format=xml'
API_XML_DRIVERS_ROUT = '/api/v1/report/drivers/?format=xml'

xml_api_test_case = [
    (0, 'SVF', 'Sebastian Vettel'),
    (9, 'CSR', 'Carlos Sainz'),
    (18, 'LHM', 'Lewis Hamilton')
]


@pytest.mark.parametrize('position, abr, _', xml_api_test_case)
def test_xml_api_report(client, position, abr, _):
    response = client.get(API_XML_REPORT_ROUT)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/xml'

    root = ElementTree.fromstring(response.data)
    assert root.tag == 'report'
    assert len(root) == DRIVER_AMOUNT
    abr_elements = root.findall('abr')
    assert abr_elements[position].text == abr


@pytest.mark.parametrize('position, _, name', xml_api_test_case)
def test_xml_api_drivers(client, position, _, name):
    response = client.get(API_XML_DRIVERS_ROUT)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/xml'

    root = ElementTree.fromstring(response.data)
    assert root.tag == 'drivers'
    assert len(root) == DRIVER_AMOUNT
    driver_elements = root.findall('driver')
    assert driver_elements[position].text == name


xml_driver_test_case = [
    ('SVF', 'Sebastian Vettel', '1', '64.415'),
    ('FAM', 'Fernando Alonso', '5', '72.657'),
    ('CSR', 'Carlos Sainz', '10', '72.95'),
    ('KMH', 'Kevin Magnussen', '15', '73.393'),
    ('LHM', 'Lewis Hamilton', '19', '-407.54')
]


@pytest.mark.parametrize('abr, name, position, lap_time', xml_driver_test_case)
def test_xml_api_driver(client, abr, name, position, lap_time):
    response = client.get(f'/api/v1/report/drivers/{abr}/?format=xml')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/xml'

    root = ElementTree.fromstring(response.data)
    assert root.tag == 'driver'
    assert root.text == name
    assert root.find('position').text == position
    assert root.find('lap_time').text == lap_time
