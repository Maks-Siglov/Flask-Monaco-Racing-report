from sqlalchemy import select

from app.db.models.reports import Driver, Result
from app.bl.report.prepare import sort_results


def test_sort_drivers(test_db_session):
    with test_db_session as session:
        worst_driver = Driver(abr='LHM', name='Lewis Hamilton', team='MERCEDES')
        best_driver = Driver(abr='NHR', name='Nico Hulkenberg', team='RENAULT')
        medium_driver = Driver(abr='KRF', name='Kimi Raikkonen', team='FERRARI')
        worst_result = Result(driver=worst_driver, minutes=-1, seconds=6.4)
        best_result = Result(driver=best_driver, minutes=1, seconds=30.2)
        medium_result = Result(driver=medium_driver, minutes=2, seconds=7.9)

        session.add_all([worst_result, medium_result, best_result])

        sort_results(session)

        statement = select(Result, Driver).join(Driver).order_by(
            Result.position)
        sorted_results = session.execute(statement).scalars().all()

        assert sorted_results[0] == best_result
        assert sorted_results[0].driver == best_driver
        assert sorted_results[1] == medium_result
        assert sorted_results[1].driver == medium_driver
        assert sorted_results[2] == worst_result
        assert sorted_results[2].driver == worst_driver
