from app.bl.report.models import Driver
from xml.etree import ElementTree
from flask import make_response, Response


def xml_response_api_report(prepared_data: list[Driver]) -> Response:
    root = ElementTree.Element('report')

    for driver in prepared_data:
        abr_element = ElementTree.SubElement(root, 'abr')
        name = ElementTree.SubElement(abr_element, 'name')
        team = ElementTree.SubElement(abr_element, 'team')

        abr_element.text = driver.abr
        name.text = driver.name
        team.text = driver.team

    response = make_response(
        ElementTree.tostring(root, encoding='utf-8').decode())
    response.headers['Content-Type'] = 'application/xml'

    return response


def xml_response_api_drivers(prepared_data: list[Driver]) -> Response:
    root = ElementTree.Element('drivers')

    for driver in prepared_data:
        _prepare_driver_xml(root, driver)

    response = make_response(
        ElementTree.tostring(root, encoding='utf-8').decode())
    response.headers['Content-Type'] = 'application/xml'

    return response


def xml_response_api_driver(driver: Driver) -> Response:
    root = ElementTree.Element('driver')

    _prepare_driver_xml(root, driver)

    response = make_response(
        ElementTree.tostring(root, encoding='utf-8').decode())
    response.headers['Content-Type'] = 'application/xml'

    return response


def _prepare_driver_xml(root: ElementTree.Element, driver: Driver) -> None:
    name_element = ElementTree.SubElement(root, 'name')
    team = ElementTree.SubElement(name_element, 'team')
    position = ElementTree.SubElement(name_element, 'position')
    lap_time = ElementTree.SubElement(name_element, 'lap_time')

    name_element.text = driver.name
    team.text = driver.team
    position.text = str(driver.position)
    lap_time.text = str(driver.lap_time.total_seconds)
