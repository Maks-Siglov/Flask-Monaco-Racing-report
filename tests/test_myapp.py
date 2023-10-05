import pytest

test_case = [
    ('Common Statistics', '/report', 200),
    ('Drivers info', '/report/drivers/', 200),
    ('Drivers info', '/report/drivers/?order=desc', 200),
    ('Path not found', '/report/drivers/?driver_id=NOT', 404)
]


@pytest.mark.parametrize('header, route, code', test_case)
def test_report(client, header, route, code):
    response = client.get(route)
    assert response.status_code == code
    assert header.encode() in response.data
