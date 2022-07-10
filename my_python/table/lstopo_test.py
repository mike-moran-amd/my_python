# encoding=UTF-8
from my_python import data
from my_python.table import lstopo, cpuinfo

TOPO_LABEL = '48 AMD EPYC 7402P 24-Core Processor'
DATA = '''Machine (62GB total)
  Package L#0
    NUMANode L#0 (P#0 62GB)
    L3 L#0 (16MB)
      L2 L#0 (512KB) + L1d L#0 (32KB) + L1i L#0 (32KB) + Core L#0
        PU L#0 (P#0)
        PU L#1 (P#24)
      L2 L#1 (512KB) + L1d L#1 (32KB) + L1i L#1 (32KB) + Core L#1
        PU L#2 (P#1)
        PU L#3 (P#25)
      L2 L#2 (512KB) + L1d L#2 (32KB) + L1i L#2 (32KB) + Core L#2
        PU L#4 (P#2)
        PU L#5 (P#26)
    L3 L#1 (16MB)
      L2 L#3 (512KB) + L1d L#3 (32KB) + L1i L#3 (32KB) + Core L#3
        PU L#6 (P#3)
        PU L#7 (P#27)
      L2 L#4 (512KB) + L1d L#4 (32KB) + L1i L#4 (32KB) + Core L#4
        PU L#8 (P#4)
        PU L#9 (P#28)
      L2 L#5 (512KB) + L1d L#5 (32KB) + L1i L#5 (32KB) + Core L#5
        PU L#10 (P#5)
        PU L#11 (P#29)
    L3 L#2 (16MB)
      L2 L#6 (512KB) + L1d L#6 (32KB) + L1i L#6 (32KB) + Core L#6
        PU L#12 (P#6)
        PU L#13 (P#30)
      L2 L#7 (512KB) + L1d L#7 (32KB) + L1i L#7 (32KB) + Core L#7
        PU L#14 (P#7)
        PU L#15 (P#31)
      L2 L#8 (512KB) + L1d L#8 (32KB) + L1i L#8 (32KB) + Core L#8
        PU L#16 (P#8)
        PU L#17 (P#32)
    L3 L#3 (16MB)
      L2 L#9 (512KB) + L1d L#9 (32KB) + L1i L#9 (32KB) + Core L#9
        PU L#18 (P#9)
        PU L#19 (P#33)
      L2 L#10 (512KB) + L1d L#10 (32KB) + L1i L#10 (32KB) + Core L#10
        PU L#20 (P#10)
        PU L#21 (P#34)
      L2 L#11 (512KB) + L1d L#11 (32KB) + L1i L#11 (32KB) + Core L#11
        PU L#22 (P#11)
        PU L#23 (P#35)
    L3 L#4 (16MB)
      L2 L#12 (512KB) + L1d L#12 (32KB) + L1i L#12 (32KB) + Core L#12
        PU L#24 (P#12)
        PU L#25 (P#36)
      L2 L#13 (512KB) + L1d L#13 (32KB) + L1i L#13 (32KB) + Core L#13
        PU L#26 (P#13)
        PU L#27 (P#37)
      L2 L#14 (512KB) + L1d L#14 (32KB) + L1i L#14 (32KB) + Core L#14
        PU L#28 (P#14)
        PU L#29 (P#38)
    L3 L#5 (16MB)
      L2 L#15 (512KB) + L1d L#15 (32KB) + L1i L#15 (32KB) + Core L#15
        PU L#30 (P#15)
        PU L#31 (P#39)
      L2 L#16 (512KB) + L1d L#16 (32KB) + L1i L#16 (32KB) + Core L#16
        PU L#32 (P#16)
        PU L#33 (P#40)
      L2 L#17 (512KB) + L1d L#17 (32KB) + L1i L#17 (32KB) + Core L#17
        PU L#34 (P#17)
        PU L#35 (P#41)
    L3 L#6 (16MB)
      L2 L#18 (512KB) + L1d L#18 (32KB) + L1i L#18 (32KB) + Core L#18
        PU L#36 (P#18)
        PU L#37 (P#42)
      L2 L#19 (512KB) + L1d L#19 (32KB) + L1i L#19 (32KB) + Core L#19
        PU L#38 (P#19)
        PU L#39 (P#43)
      L2 L#20 (512KB) + L1d L#20 (32KB) + L1i L#20 (32KB) + Core L#20
        PU L#40 (P#20)
        PU L#41 (P#44)
    L3 L#7 (16MB)
      L2 L#21 (512KB) + L1d L#21 (32KB) + L1i L#21 (32KB) + Core L#21
        PU L#42 (P#21)
        PU L#43 (P#45)
      L2 L#22 (512KB) + L1d L#22 (32KB) + L1i L#22 (32KB) + Core L#22
        PU L#44 (P#22)
        PU L#45 (P#46)
      L2 L#23 (512KB) + L1d L#23 (32KB) + L1i L#23 (32KB) + Core L#23
        PU L#46 (P#23)
        PU L#47 (P#47)
  HostBridge
    PCIBridge
      PCI 01:00.0 (SAS)
        Block(Disk) "sdb"
        Block(Disk) "sda"
  HostBridge
    PCIBridge
      PCI 41:00.0 (Ethernet)
        Net "ens3f0"
      PCI 41:00.1 (Ethernet)
        Net "ens3f1"
  HostBridge
    PCIBridge
      PCI 85:00.0 (SATA)
    PCIBridge
      PCI 86:00.0 (SATA)
  HostBridge
    PCIBridge
      PCI c3:00.0 (SATA)
        Block(Disk) "sdd"
        Block(Disk) "sdc"
    PCIBridge
      PCIBridge
        PCI c2:00.0 (VGA)
'''
RESULT = '''48 AMD EPYC 7402P 24-Core Processor | Package | NUMANode | L3 | L2 | L1d | L1i | Core | PU
                                  0 |       0 |        0 |  0 |  0 |   0 |   0 |    0 |  0
                                  1 |       0 |        0 |  0 |  0 |   0 |   0 |    0 | 24
                                  2 |       0 |        0 |  0 |  1 |   1 |   1 |    1 |  1
                                  3 |       0 |        0 |  0 |  1 |   1 |   1 |    1 | 25
                                  4 |       0 |        0 |  0 |  2 |   2 |   2 |    2 |  2
                                  5 |       0 |        0 |  0 |  2 |   2 |   2 |    2 | 26
                                  6 |       0 |        0 |  1 |  3 |   3 |   3 |    3 |  3
                                  7 |       0 |        0 |  1 |  3 |   3 |   3 |    3 | 27
                                  8 |       0 |        0 |  1 |  4 |   4 |   4 |    4 |  4
                                  9 |       0 |        0 |  1 |  4 |   4 |   4 |    4 | 28
                                 10 |       0 |        0 |  1 |  5 |   5 |   5 |    5 |  5
                                 11 |       0 |        0 |  1 |  5 |   5 |   5 |    5 | 29
                                 12 |       0 |        0 |  2 |  6 |   6 |   6 |    6 |  6
                                 13 |       0 |        0 |  2 |  6 |   6 |   6 |    6 | 30
                                 14 |       0 |        0 |  2 |  7 |   7 |   7 |    7 |  7
                                 15 |       0 |        0 |  2 |  7 |   7 |   7 |    7 | 31
                                 16 |       0 |        0 |  2 |  8 |   8 |   8 |    8 |  8
                                 17 |       0 |        0 |  2 |  8 |   8 |   8 |    8 | 32
                                 18 |       0 |        0 |  3 |  9 |   9 |   9 |    9 |  9
                                 19 |       0 |        0 |  3 |  9 |   9 |   9 |    9 | 33
                                 20 |       0 |        0 |  3 | 10 |  10 |  10 |   10 | 10
                                 21 |       0 |        0 |  3 | 10 |  10 |  10 |   10 | 34
                                 22 |       0 |        0 |  3 | 11 |  11 |  11 |   11 | 11
                                 23 |       0 |        0 |  3 | 11 |  11 |  11 |   11 | 35
                                 24 |       0 |        0 |  4 | 12 |  12 |  12 |   12 | 12
                                 25 |       0 |        0 |  4 | 12 |  12 |  12 |   12 | 36
                                 26 |       0 |        0 |  4 | 13 |  13 |  13 |   13 | 13
                                 27 |       0 |        0 |  4 | 13 |  13 |  13 |   13 | 37
                                 28 |       0 |        0 |  4 | 14 |  14 |  14 |   14 | 14
                                 29 |       0 |        0 |  4 | 14 |  14 |  14 |   14 | 38
                                 30 |       0 |        0 |  5 | 15 |  15 |  15 |   15 | 15
                                 31 |       0 |        0 |  5 | 15 |  15 |  15 |   15 | 39
                                 32 |       0 |        0 |  5 | 16 |  16 |  16 |   16 | 16
                                 33 |       0 |        0 |  5 | 16 |  16 |  16 |   16 | 40
                                 34 |       0 |        0 |  5 | 17 |  17 |  17 |   17 | 17
                                 35 |       0 |        0 |  5 | 17 |  17 |  17 |   17 | 41
                                 36 |       0 |        0 |  6 | 18 |  18 |  18 |   18 | 18
                                 37 |       0 |        0 |  6 | 18 |  18 |  18 |   18 | 42
                                 38 |       0 |        0 |  6 | 19 |  19 |  19 |   19 | 19
                                 39 |       0 |        0 |  6 | 19 |  19 |  19 |   19 | 43
                                 40 |       0 |        0 |  6 | 20 |  20 |  20 |   20 | 20
                                 41 |       0 |        0 |  6 | 20 |  20 |  20 |   20 | 44
                                 42 |       0 |        0 |  7 | 21 |  21 |  21 |   21 | 21
                                 43 |       0 |        0 |  7 | 21 |  21 |  21 |   21 | 45
                                 44 |       0 |        0 |  7 | 22 |  22 |  22 |   22 | 22
                                 45 |       0 |        0 |  7 | 22 |  22 |  22 |   22 | 46
                                 46 |       0 |        0 |  7 | 23 |  23 |  23 |   23 | 23
                                 47 |       0 |        0 |  7 | 23 |  23 |  23 |   23 | 47'''


def test_generate_topology():
    t = lstopo.LsTopoTable.from_text(DATA)
    print('\n')
    print(t.pf(TOPO_LABEL))
    assert t.pf(TOPO_LABEL) == RESULT
    t.print_golang_struct(TOPO_LABEL)


def test_test():
    print()
    # name = 'mm15'  # AMD_EPYC_7402P_24_Core_Processor
    # name = 'mm16'  # AMD_EPYC_7502P_32_Core_Processor
    # name = 'mm17'  # Intel_R__Xeon_R__E_2278G_CPU___3_40GHz
    # name = 'mm18'  #  Intel_R__Xeon_R__Silver_4214_CPU___2_20GHz
    # name = 'mm19'  # AMD_EPYC_7513_32_Core_Processor
    # name = 'mm20'  #  REPEAT AMD_EPYC_7502P_32_Core_Processor
    # name = 'mm21'  #  REPEAT Intel_R__Xeon_R__E_2278G_CPU___3_40GHz
    # name = 'mm22'  #  AMD_EPYC_7443P_24_Core_Processor
    # name = 'mm27'  #  Intel_R__Xeon_R__E_2378G_CPU___2_80GHz
    # name = 'mm28'  #  REPEAT AMD_EPYC_7402P_24_Core_Processor
    # name = 'mm29'  #  FIXME
    # name = 'mm30'  # Intel_R__Xeon_R__Gold_5120_CPU___2_20GHz
    name = 'mm36'  # AMD_EPYC_7502P_32_Core_Processor
    session_data = data.text_from(name)
    st = data.SessionData(session_data).session_table()
    print(st.pf(title='block', cols=['cwd', 'command', 'count']))

    last_lstopo_row = None
    last_cpuinfo_row = None
    for row in st.row_gen():
        if st.get_val(row, 'command') == 'lstopo':
            last_lstopo_row = row
        if st.get_val(row, 'command') == 'cat /proc/cpuinfo':
            last_cpuinfo_row = row

    if last_cpuinfo_row:
        cpu_lines = st.get_val(last_cpuinfo_row, 'lines')
        cpu_table = cpuinfo.from_text('\n'.join(cpu_lines))
        cpu_pf = cpu_table.topology_table().pf('cpu_pf')
        print()
        print(cpu_pf)

    if last_lstopo_row:
        lstopo_lines = st.get_val(last_lstopo_row, 'lines')
        lstopo_table = lstopo.LsTopoTable.from_text('\n'.join(lstopo_lines))
        lstopo_pf = lstopo_table.pf('lstopo_pf')
        print()
        print(lstopo_pf)

        model_name = cpu_table.get_val(0, 'model name') if last_cpuinfo_row else 'UNKNOWN'
        model_name = model_name.replace(' ', '_')
        model_name = model_name.replace('-', '_')
        model_name = model_name.replace('(', '_')
        model_name = model_name.replace(')', '_')
        model_name = model_name.replace('@', '_')
        model_name = model_name.replace('.', '_')
        print()
        print(model_name)
        lstopo_table.print_golang_struct(model_name)
