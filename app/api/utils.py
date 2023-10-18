from app.bl.report.models import Driver
from xml.etree import ElementTree
from flask import make_response, Response


def json_data_for_report(prepared_data: list[Driver]) -> dict:
    return {
        driver.abr: _prepare_driver_for_json(driver) for driver in prepared_data
            }


def json_data_for_driver(driver: Driver) -> dict:
    return {driver.abr: _prepare_driver_for_json(driver)}


def _prepare_driver_for_json(driver: Driver) -> dict:
    json_driver = {
            'position': driver.position,
            'name': driver.name,
            'team': driver.team,
            'lap_time': [driver.lap_time.minutes, driver.lap_time.seconds]
    }
    return json_driver


def xml_response_for_report(prepared_data: list[Driver]) -> Response:
    root = ElementTree.Element('drivers')

    for driver in prepared_data:
        driver_element = ElementTree.SubElement(root, 'driver')

        _prepare_driver_for_xml(driver_element, driver)

    response = make_response(
        ElementTree.tostring(root, encoding='utf-8').decode())
    response.headers['Content-Type'] = 'application/xml'

    return response


def xml_response_for_driver(driver: Driver) -> Response:
    root = ElementTree.Element('driver')

    _prepare_driver_for_xml(root, driver)

    response = make_response(
        ElementTree.tostring(root, encoding='utf-8').decode())
    response.headers['Content-Type'] = 'application/xml'

    return response


def _prepare_driver_for_xml(root: ElementTree.Element, driver: Driver) -> None:

    position = ElementTree.SubElement(root, 'position')
    abr = ElementTree.SubElement(root, 'abr')
    name = ElementTree.SubElement(root, 'name')
    team = ElementTree.SubElement(root, 'team')
    lap_time_element = ElementTree.SubElement(root, 'lap_time')
    minutes = ElementTree.SubElement(lap_time_element, 'minutes')
    seconds = ElementTree.SubElement(lap_time_element, 'seconds')

    position.text = str(driver.position)
    abr.text = driver.abr
    name.text = driver.name
    team.text = driver.team
    minutes.text = str(driver.lap_time.minutes)
    seconds.text = str(driver.lap_time.seconds)
