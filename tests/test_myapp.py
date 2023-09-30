import pytest

test_case = [('Common Statistics', '/report'), ('Drivers code', '/report/drivers/'),
             ('Drivers code', '/report/drivers/?order=desc'), ('Driver Details', '/report/drivers/SPF')]


@pytest.mark.parametrize('header, route', test_case)
def test_report(client, header, route):
    response = client.get(route)
    assert response.status_code == 200
    assert header.encode() in response.data


not_exist_route_cases = [('non/existing/route', 404), ('/report/drivers/NOT', 404)]


@pytest.mark.parametrize('route, status_code', not_exist_route_cases)
def test_not_exist_route(client, route, status_code):
    response = client.get(route)
    assert response.status_code == status_code
