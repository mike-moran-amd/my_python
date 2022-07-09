#!python3
# encoding=UTF-8
import pathlib
from my_python.table import cpuinfo


def get_table(name='cpuinfo_test_epyc_7513'):
    fp = pathlib.Path(__file__).parent
    fp = pathlib.Path(fp, name)
    t = cpuinfo.from_file(fp)
    return t


def test_cpuinfo_from_file():
    t = get_table()
    print('\n')
    print(t.pf(title='TABLE'))
    d, s = t.split_static()
    print(s.pf(title='STATIC'))
    print(d.pf(title='DELTA*'))


def test_initial_apicid_equals_apicid():
    t = get_table()
    print('\n')

    for row in t.row_gen():
        # determine if "apicid" and "initial apicid" are the same
        val = t.get_val(row, 'apicid')
        val2 = t.get_val(row, 'initial apicid')
        assert val == val2


def test_generate_topology():
    t = get_table()
    print('\n')

    tt = t.topology_table()
    tt.print_struct('name')
