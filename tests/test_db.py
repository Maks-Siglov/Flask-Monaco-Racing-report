from app.db.models import Driver, Result
from app.bl.report.prepare import sort_results


def test_insert_data(test_db):
    driver = Driver.create(
        abr='SPF', name='Sergio Perez', team='FORCE INDIA MERCEDES')
    result = Result.create(owner=driver, minutes=2, seconds=4)
    item = Driver.get(abr='SPF')
    assert item.name == 'Sergio Perez'
    assert result.owner == driver


def test_sort_drivers(test_db):
    driver1 = Driver.create(abr='LHM', name='Lewis Hamilton', team='MERCEDES')
    driver2 = Driver.create(abr='NHR', name='Nico Hulkenberg', team='RENAULT')
    driver3 = Driver.create(abr='KRF', name='Kimi Raikkonen', team='FERRARI')
    worst_result = Result.create(owner=driver1, minutes=-1, seconds=6.4)
    best_result = Result.create(owner=driver2, minutes=1, seconds=30.2)
    medium_result = Result.create(owner=driver3, minutes=2, seconds=7.9)

    sort_results()

    sorted_results = Result.select().order_by(Result.position)
    assert sorted_results[0] == best_result
    assert sorted_results[1] == medium_result
    assert sorted_results[2] == worst_result
