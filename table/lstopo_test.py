# encoding=UTF-8
import data
from table import lstopo, cpuinfo


DATA = '''Machine (31GB total)
  Package L#0
    NUMANode L#0 (P#0 31GB)
    L3 L#0 (16MB)
      L2 L#0 (256KB) + L1d L#0 (32KB) + L1i L#0 (32KB) + Core L#0 + PU L#0 (P#0)
      L2 L#1 (256KB) + L1d L#1 (32KB) + L1i L#1 (32KB) + Core L#1 + PU L#1 (P#1)
      L2 L#2 (256KB) + L1d L#2 (32KB) + L1i L#2 (32KB) + Core L#2 + PU L#2 (P#2)
      L2 L#3 (256KB) + L1d L#3 (32KB) + L1i L#3 (32KB) + Core L#3 + PU L#3 (P#3)
      L2 L#4 (256KB) + L1d L#4 (32KB) + L1i L#4 (32KB) + Core L#4 + PU L#4 (P#4)
      L2 L#5 (256KB) + L1d L#5 (32KB) + L1i L#5 (32KB) + Core L#5 + PU L#5 (P#5)
      L2 L#6 (256KB) + L1d L#6 (32KB) + L1i L#6 (32KB) + Core L#6 + PU L#6 (P#6)
      L2 L#7 (256KB) + L1d L#7 (32KB) + L1i L#7 (32KB) + Core L#7 + PU L#7 (P#7)
  HostBridge
    PCIBridge
      PCI 01:00.0 (Ethernet)
        Net "enp1s0f0"
        OpenFabrics "mlx5_bond_0"
      PCI 01:00.1 (Ethernet)
        Net "enp1s0f1"
    PCI 00:17.0 (SATA)
      Block(Disk) "sdb"
      Block(Disk) "sda"
    PCIBridge
      PCI 03:00.0 (Ethernet)
        Net "eno1"
    PCIBridge
      PCI 04:00.0 (Ethernet)
        Net "eno2"
    PCIBridge
      PCIBridge
        PCI 07:00.0 (VGA)
'''

def test_generate_topology():
    t = lstopo.LsTopoTable.from_text(DATA)
    print('\n')

    print(t.pf(''))
    t.print_golang_struct('mm27')
    #tt.print_struct('name')

def test_test():
    print()
    #name = 'mm15'  # AMD_EPYC_7402P_24_Core_Processor
    #name = 'mm16'  # AMD_EPYC_7502P_32_Core_Processor
    #name = 'mm17'  # Intel_R__Xeon_R__E_2278G_CPU___3_40GHz
    #name = 'mm18'  #  Intel_R__Xeon_R__Silver_4214_CPU___2_20GHz
    #name = 'mm19'  # AMD_EPYC_7513_32_Core_Processor
    #name = 'mm20'  #  REPEAT AMD_EPYC_7502P_32_Core_Processor
    #name = 'mm21'  #  REPEAT Intel_R__Xeon_R__E_2278G_CPU___3_40GHz
    #name = 'mm22'  #  AMD_EPYC_7443P_24_Core_Processor
    #name = 'mm27'  #  Intel_R__Xeon_R__E_2378G_CPU___2_80GHz
    #name = 'mm28'  #  REPEAT AMD_EPYC_7402P_24_Core_Processor
    #name = 'mm29'  #  FIXME
    name = 'mm30'  # Intel_R__Xeon_R__Gold_5120_CPU___2_20GHz
    session_data = data.string_from(name)
    st = data.SessionData(session_data).session_table()
    print(st.pf(title='block', cols=['cwd', 'command', 'count']))

    last_lstopo_row = None
    last_cpuinfo_row = None
    for row in st.row_gen():
        if st.get_val(row, 'command') == 'lstopo':
            last_lstopo_row = row
        if st.get_val(row, 'command') == 'cat /proc/cpuinfo':
            last_cpuinfo_row = row

    if last_lstopo_row and last_cpuinfo_row:
        cpu_lines = st.get_val(last_cpuinfo_row, 'lines')
        cpu_table = cpuinfo.from_text('\n'.join(cpu_lines))
        cpu_pf = cpu_table.topology_table().pf(name)
        print()
        print(cpu_pf)

        lstopo_lines = st.get_val(last_lstopo_row, 'lines')
        lstopo_table = lstopo.LsTopoTable.from_text('\n'.join(lstopo_lines))
        lstopo_pf = lstopo_table.pf(name)
        print()
        print(lstopo_pf)

        print()
        model_name = cpu_table.get_val(0, 'model name')
        model_name = model_name.replace(' ', '_')
        model_name = model_name.replace('-', '_')
        model_name = model_name.replace('(', '_')
        model_name = model_name.replace(')', '_')
        model_name = model_name.replace('@', '_')
        model_name = model_name.replace('.', '_')
        print(model_name)
        lstopo_table.print_golang_struct(model_name)
        assert lstopo_pf == cpu_pf