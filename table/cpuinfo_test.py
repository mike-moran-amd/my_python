import lib
import pathlib
from table import cpuinfo


def test_cpuinfo_from_file():
    fp = pathlib.Path(__file__).parent
    fp = pathlib.Path(fp, 'cpuinfo_test_data')
    t = cpuinfo.from_file(fp)
    print('\n')
    print(t.pf(title='TABLE'))
    s, d = t.split_dynamic_static()
    print(s.pf(title='STATIC'))
    print(d.pf(title='DELTA*'))
    pass
