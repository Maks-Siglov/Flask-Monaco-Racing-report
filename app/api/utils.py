from app.bl.report.models import Driver


def json_data_for_report(prepared_data: list[Driver]) -> dict:
    json_data = {
        driver.abr: {
            'position': driver.position,
            'name': driver.name,
            'team': driver.team,
            'lap_time': [driver.lap_time.minutes, driver.lap_time.seconds]
        }
        for driver in prepared_data}

    return json_data


def json_data_for_driver(driver: Driver) -> dict:
    lap_time = [driver.lap_time.minutes, driver.lap_time.seconds]
    json_data = {
        'position': driver.position,
        'abr': driver.abr,
        'name': driver.name,
        'team': driver.team,
        'lap_time': lap_time
    }
    return json_data
