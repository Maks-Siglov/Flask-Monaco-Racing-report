import pytest

routes_test_case = [
    ('Common Statistics', '/', 200),
    ('Common Statistics', '/report/', 200),
    ('Drivers info', '/report/drivers/', 200),
    ('Drivers info', '/report/drivers/?order=desc', 200),
    ('Driver Statistics', '/report/drivers/SPF', 200),
]


@pytest.mark.parametrize('header, route, expected_code', routes_test_case)
def test_report(client, header, route, expected_code):
    response = client.get(route)
    assert response.status_code == expected_code
    assert header.encode() in response.data


test_case_404 = [('Path not found', '/report/drivers/NOT', 404)]


@pytest.mark.parametrize('header, route, expected_code', test_case_404)
def test_driver_404(client, header, route, expected_code):
    response = client.get(route)
    assert response.status_code == expected_code
    assert header.encode() in response.data
