import logging

FORMAT = ' | '.join([
        '%(asctime)s',
        '%(levelname)s',
        '%(process)d',
        '%(threadName)s %(thread)d',
        '%(name)s %(lineno)d',
        '%(message)s',
        ])

DATE_FORMAT = '%b %d %Y %H:%M:%S'


def start_logging(level=logging.INFO, format=FORMAT, datefmt=DATE_FORMAT, force=False, **kwargs):
    """
    >>> start_logging(level=logging.DEBUG)  # log everything

    The output of the above command is sent to stderr so it is not printed above, but below is the output from stderr
    Jan 18 2023 15:33:59 | DEBUG | 6282 | MainThread 4566642176 | root 35 | LOGGING STARTED

    >>> FORMAT
    '%(asctime)s | %(levelname)s | %(process)d | %(threadName)s %(thread)d | %(name)s %(lineno)d | %(message)s'

    >>> DATE_FORMAT
    '%b %d %Y %H:%M:%S'

    """
    logging.basicConfig(
        format=format,
        datefmt=datefmt,
        level=level,
        force=force,
        **kwargs)
    logging.debug(f'start_logging(level={level}, format={format}, datefmt={datefmt}, force={force}, kwargs={kwargs})')
