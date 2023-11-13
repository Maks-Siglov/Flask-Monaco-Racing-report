

from typing import Sequence
from xml.etree import ElementTree
from sqlalchemy import Row

from flask import (
    Response,
    make_response,
)
from app.db.models import (
    Result,
    Driver
)


def xml_response_api_report(query_result: Sequence[Driver]) -> Response:
    """This function generate xml response for /api/v1/report?format=xml

    :param query_result: Sequence with Drivers through which we can iterate and
    take drivers
    """
    root = ElementTree.Element('report')

    for driver in query_result:
        abbr_element = ElementTree.SubElement(root, 'abbr')
        name = ElementTree.SubElement(abbr_element, 'name')
        team = ElementTree.SubElement(abbr_element, 'team')

        abbr_element.text = driver.abbr
        name.text = driver.name
        team.text = driver.team.name

    response = make_response(
        ElementTree.tostring(root, encoding='utf-8').decode()
    )
    response.headers['Content-Type'] = 'application/xml'

    return response


def xml_response_api_drivers(
    query_result: Sequence[Row[tuple[Result, Driver]]]
) -> Response:
    """This function generate xml response for
    /api/v1/report/drivers?format=xml
    """
    root = ElementTree.Element('drivers')

    for result, driver in query_result:
        driver_element = ElementTree.SubElement(root, 'driver')
        _prepare_driver_xml(driver_element, result, driver)

    response = make_response(
        ElementTree.tostring(root, encoding='utf-8').decode()
    )
    response.headers['Content-Type'] = 'application/xml'

    return response


def xml_response_api_driver(result: Result, driver: Driver) -> Response:
    """This function generate xml response for
    /api/v1/report/drivers/<string:driver_id>?format=xml
    """
    driver_element = ElementTree.Element('driver')

    _prepare_driver_xml(driver_element, result, driver)

    response = make_response(
        ElementTree.tostring(driver_element, encoding='utf-8').decode()
    )
    response.headers['Content-Type'] = 'application/xml'

    return response


def _prepare_driver_xml(
    driver_element: ElementTree.Element, result: Result, driver: Driver
) -> None:
    """This function prepare xml data about single driver, it takes
    driver_element (element of xml ElementTree), add subElements and values
    (text) to it for forming xml tree for xml_response_api_drivers/driver

    :param driver_element: element to whom we add subElements and value
    :param result: result object which contains data about driver result
    :param driver: driver object which contains data about drivers abbr, team,
    name
    """
    team = ElementTree.SubElement(driver_element, 'team')
    position = ElementTree.SubElement(driver_element, 'position')
    lap_time = ElementTree.SubElement(driver_element, 'lap_time')

    driver_element.text = driver.name
    team.text = driver.team.name
    position.text = str(result.position)
    lap_time.text = str(result.total_seconds)
