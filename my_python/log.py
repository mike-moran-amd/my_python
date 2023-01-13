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


def start_logging(logging_level=logging.INFO, logging_format=FORMAT, logging_date_format=DATE_FORMAT, force=False):
    """
    >>> start_logging(logging_level=logging.NOTSET)  # log everything

    The output of the above command is sent to stderr so it is not printed above, but below is the output from stderr
    Jan 13 2023 16:46:21 - DEBUG - 2577 - MainThread 4373798400 - root 36 - LOGGING STARTED

    >>> FORMAT
    '%(asctime)s | %(levelname)s | %(process)d | %(threadName)s %(thread)d | %(name)s %(lineno)d | %(message)s'

    >>> DATE_FORMAT
    '%b %d %Y %H:%M:%S'

    """
    logging.basicConfig(
        format = logging_format,
        datefmt = logging_date_format,
        level = logging_level,
        force=force,
        )
    logging.log(logging.DEBUG, f'LOGGING STARTED')
