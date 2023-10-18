from app.bl.report.models import Driver


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
