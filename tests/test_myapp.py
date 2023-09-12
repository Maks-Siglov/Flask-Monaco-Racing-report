import pytest

test_case = [('Common Statistics', '/report'), ('Drivers code', '/report/drivers/')]


@pytest.mark.parametrize('data, route', test_case)
def test_report(client, data, route):
    response = client.get(route)
    assert response.status_code == 200
    assert data.encode() in response.data
