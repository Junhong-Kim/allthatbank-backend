from datetime import datetime


def datetime_formatter(datetime_str, datetime_format):
    return datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%f').strftime(datetime_format)
