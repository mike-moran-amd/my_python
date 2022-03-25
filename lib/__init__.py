#!/usr/bin/python
# encoding=UTF-8
import datetime
from table import Table


def dt_str(dt=None):
    """
    Creates a timestamp that is sorta readable but uniquely sortable
    :param dt: datetime or None (default) to use now()
    :return: 18 character string with 2 digits (zero filled) for year, month, day, ..., and 6 for the microsecond

    For example:
    >>> dt_str(datetime.datetime(2022, 3, 24, 19, 23, 0, 123456))
    '220324192300123456'

    """
    dt = dt or datetime.datetime.now()
    return '%0.2d' * 6 % (dt.year % 100, dt.month, dt.day, dt.hour, dt.minute, dt.second) + '%0.6d' % dt.microsecond
