from datetime import timedelta


def format_timedelta(timedelta_obj: timedelta) -> tuple[int, float]:
    """This function convert timedelta object into tuple with numbers for report

    :param timedelta_obj: timedelta result of subtraction of time of end lap and
     start lap
    :return: namedtuple with minutes and seconds (int and float)
    """
    minutes, seconds = divmod(timedelta_obj.total_seconds(), 60)

    return int(minutes), round(seconds, 3)
