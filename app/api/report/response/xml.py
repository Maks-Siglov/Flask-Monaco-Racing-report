from flask import make_response, Response
from xml.etree import ElementTree

from app.db.models import Result


def xml_response_api_report(prepared_data: list[tuple[Result.owner, Result]]
                            ) -> Response:
    """This function generate xml response for /api/v1/report/?format=xml

    :param prepared_data: list with tuples which contains two object, first -
    driver with it name, abr and team, second - result with driver results in
    race (position, time)
    """
    root = ElementTree.Element('report')

    for driver, _ in prepared_data:
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


def xml_response_api_drivers(prepared_data: list[tuple[Result.owner, Result]]
                             ) -> Response:
    """This function generate xml response for
    /api/v1/report/drivers/?format=xml
     """
    root = ElementTree.Element('drivers')

    for driver, result in prepared_data:
        driver_element = ElementTree.SubElement(root, 'driver')
        _prepare_driver_xml(driver_element, driver, result)

    response = make_response(
        ElementTree.tostring(root, encoding='utf-8').decode())
    response.headers['Content-Type'] = 'application/xml'

    return response


def xml_response_api_driver(driver: Result.owner, result: Result) -> Response:
    """This function generate xml response for
     /api/v1/report/drivers/<string:driver_id>/?format=xml
     """
    driver_element = ElementTree.Element('driver')

    _prepare_driver_xml(driver_element, driver, result)

    response = make_response(
        ElementTree.tostring(driver_element, encoding='utf-8').decode())
    response.headers['Content-Type'] = 'application/xml'

    return response


def _prepare_driver_xml(driver_element: ElementTree.Element,
                        driver: Result.owner, result: Result) -> None:
    """This function prepare xml data about single driver, it takes
     driver_element (element of xml ElementTree), add subElements and values
    (text) to it for forming xml tree for xml_response_api_drivers/driver

     :param driver_element: element to whom we add subElements and value
     :param driver: driver object, that contains name, abr, team
     :param result: result object which belong to driver, contains driver
      position, and time results in race
     """
    team = ElementTree.SubElement(driver_element, 'team')
    position = ElementTree.SubElement(driver_element, 'position')
    lap_time = ElementTree.SubElement(driver_element, 'lap_time')

    driver_element.text = driver.name
    team.text = driver.team
    position.text = str(result.position)
    lap_time.text = str(result.total_seconds)
