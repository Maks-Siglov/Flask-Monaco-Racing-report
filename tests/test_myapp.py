import pytest

test_case = [('Common Statistics', '/report'), ('Drivers code', '/report/drivers/'), ('Drivers code', '/report/drivers/?order=desc'), ('Driver Details', '/report/drivers/SPF')]


@pytest.mark.parametrize('header, route', test_case)
def test_report(client, header, route):
    response = client.get(route)
    assert response.status_code == 200
    assert header.encode() in response.data
