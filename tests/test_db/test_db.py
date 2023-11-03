from sqlalchemy import select
from datetime import datetime

from app.db.models.reports import Driver, Result
from app.bl.report.prepare import sort_results
from app.db.utils import drop_table, create_table

DATE_FORMAT = '%Y-%m-%d_%H:%M:%S.%f'

START_BEST_DRIVER = datetime.strptime('2018-05-24_12:14:12.05', DATE_FORMAT)
END_BEST_DRIVER = datetime.strptime('2018-05-24_15:14:12.77', DATE_FORMAT)

START_WORST_DRIVER = datetime.strptime('2018-05-24_12:14:12.22', DATE_FORMAT)
END_WORST_DRIVER = datetime.strptime('2018-05-24_11:14:12.226', DATE_FORMAT)


def test_sort_drivers(test_session, clean_up_database):

    worst_driver = Driver(abr='LHM', name='Lewis Hamilton', team='MERCEDES')
    best_driver = Driver(abr='NHR', name='Nico Hulkenberg', team='RENAULT')

    worst_result = Result(driver=worst_driver, start=START_WORST_DRIVER,
                              end=END_WORST_DRIVER)
    best_result = Result(driver=best_driver, start=START_BEST_DRIVER,
                             end=END_BEST_DRIVER)

    test_session.user_db.add_all([worst_result, best_result])

    sort_results(test_session.user_db)

    statement = select(Result, Driver).join(Driver).order_by(
            Result.position)
    sorted_results = test_session.user_db.execute(statement).scalars().all()

    assert sorted_results[0] == best_result
    assert sorted_results[0].driver == best_driver
    assert sorted_results[1] == worst_result
    assert sorted_results[1].driver == worst_driver
