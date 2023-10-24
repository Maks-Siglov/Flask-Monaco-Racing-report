from app.db.models.reports import Driver, Result
from app.bl.report.prepare import sort_results


def test_insert_data(test_db_session):
    with test_db_session as session:
        driver = Driver(
            abr='SPF', name='Sergio Perez', team='FORCE INDIA MERCEDES')
        result = Result(owner=driver, minutes=2, seconds=4)
        session.add(driver)
        session.add(result)
        item = session.query(Driver).filter_by(abr='SPF').first()
    assert item.name == 'Sergio Perez'
    assert result.owner == item
