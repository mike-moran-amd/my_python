#!python3
# encoding=utf-8
import datetime

from lib import prime


class FakeArgs:
    def __init__(self, nth=None, seconds=None):
        self.nth = nth
        self.seconds = seconds


def test_prime_main_nth(mocker):
    mocker.patch('argparse.ArgumentParser.parse_args', return_value=FakeArgs(nth=1000))

    x = prime.main()

    assert x == 7919


def test_prime_main_timed(mocker):
    mocker.patch('argparse.ArgumentParser.parse_args', return_value=FakeArgs(seconds=3))
    before = datetime.datetime.now()

    x = prime.main()

    after = datetime.datetime.now()
    td = after - before
    assert 2 < td.seconds < 4
    print(x)
