from flask import make_response, Response
from xml.etree import ElementTree

from app.bl.report.models import Driver


def xml_response_api_report(prepared_data: list[Driver]) -> Response:
    """This function generate xml response for /api/v1/report/?format=xml"""
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
    """This function generate xml response for
    /api/v1/report/drivers/?format=xml
     """
    root = ElementTree.Element('drivers')

    for driver in prepared_data:
        driver_element = ElementTree.SubElement(root, 'driver')
        _prepare_driver_xml(driver_element, driver)

    response = make_response(
        ElementTree.tostring(root, encoding='utf-8').decode())
    response.headers['Content-Type'] = 'application/xml'

    return response


def xml_response_api_driver(driver: Driver) -> Response:
    """This function generate xml response for
     /api/v1/report/drivers/<string:driver_id>/?format=xml
     """
    driver_element = ElementTree.Element('driver')

    _prepare_driver_xml(driver_element, driver)

    response = make_response(
        ElementTree.tostring(driver_element, encoding='utf-8').decode())
    response.headers['Content-Type'] = 'application/xml'

    return response


def _prepare_driver_xml(driver_element: ElementTree.Element,
                        driver: Driver) -> None:
    """This function prepare xml data about single driver, it takes
     driver_element (element of xml ElementTree), add subElements and values
    (text) to it for forming xml tree for xml_response_api_drivers/driver

     :param driver_element: element to whom we add subElements and value
     """
    team = ElementTree.SubElement(driver_element, 'team')
    position = ElementTree.SubElement(driver_element, 'position')
    lap_time = ElementTree.SubElement(driver_element, 'lap_time')

    driver_element.text = driver.name
    team.text = driver.team
    position.text = str(driver.position)
    lap_time.text = str(driver.lap_time.total_seconds)
