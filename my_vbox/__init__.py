#!python3
# encoding=UTF-8
"""

"""
import pathlib
import lib


NL = '\n'


class MyBox:
    def __init__(self):
        """
        >>> mb = MyBox()
        """
        self.__vbox_path = lib.path_for_command('vboxmanage')

    def list_vms(self):
        """
        >>> for line in MyBox().list_vms().split(NL):
        ...     print(line.strip())
        "centos_default_1646280262092_51162" {18748b24-afea-4945-a02c-6ee9c70f9ddf}
        "centos8" {ca6d485f-33d1-4f66-8df3-a3be3b1970ff}
        <BLANKLINE>
        """
        return lib.invoke_subprocess([self.__vbox_path, 'list', 'vms'])

    def list_runningvms(self, long=False):
        """
        >>> for line in MyBox().list_runningvms().split(NL):
        ...     print(line.strip())
        "centos8" {ca6d485f-33d1-4f66-8df3-a3be3b1970ff}
        <BLANKLINE>

        >>> for line in MyBox().list_runningvms(long=True).split(NL):
        ...     print(line.strip())
        Name:                        centos8
        Groups:                      /
        Guest OS:                    Red Hat (64-bit)
        UUID:                        ca6d485f-33d1-4f66-8df3-a3be3b1970ff
        Config file:                 /Users/mfm/VirtualBox VMs/centos8/centos8.vbox
        Snapshot folder:             /Users/mfm/VirtualBox VMs/centos8/Snapshots
        Log folder:                  /Users/mfm/VirtualBox VMs/centos8/Logs
        Hardware UUID:               ca6d485f-33d1-4f66-8df3-a3be3b1970ff
        Memory size:                 2048MB
        Page Fusion:                 disabled
        VRAM size:                   32MB
        CPU exec cap:                100%
        HPET:                        disabled
        CPUProfile:                  host
        Chipset:                     piix3
        Firmware:                    BIOS
        Number of CPUs:              2
        PAE:                         enabled
        Long Mode:                   enabled
        Triple Fault Reset:          disabled
        APIC:                        enabled
        X2APIC:                      enabled
        Nested VT-x/AMD-V:           disabled
        CPUID Portability Level:     0
        CPUID overrides:             None
        Boot menu mode:              message and menu
        Boot Device 1:               HardDisk
        Boot Device 2:               DVD
        Boot Device 3:               Not Assigned
        Boot Device 4:               Not Assigned
        ACPI:                        enabled
        IOAPIC:                      enabled
        BIOS APIC mode:              APIC
        Time offset:                 0ms
        RTC:                         UTC
        Hardware Virtualization:     enabled
        Nested Paging:               enabled
        Large Pages:                 disabled
        VT-x VPID:                   enabled
        VT-x Unrestricted Exec.:     enabled
        Paravirt. Provider:          Default
        Effective Paravirt. Prov.:   KVM
        State:                       running (since 2022-04-02T22:10:09.870000000)
        Graphics Controller:         VBoxVGA
        Monitor count:               1
        3D Acceleration:             disabled
        2D Video Acceleration:       disabled
        Teleporter Enabled:          disabled
        Teleporter Port:             0
        Teleporter Address:
        Teleporter Password:
        Tracing Enabled:             disabled
        Allow Tracing to Access VM:  disabled
        Tracing Configuration:
        Autostart Enabled:           disabled
        Autostart Delay:             0
        Default Frontend:
        VM process priority:         default
        Storage Controller Name (0):            IDE Controller
        Storage Controller Type (0):            PIIX4
        Storage Controller Instance Number (0): 0
        Storage Controller Max Port Count (0):  2
        Storage Controller Port Count (0):      2
        Storage Controller Bootable (0):        on
        IDE Controller (0, 0): /Users/mfm/VirtualBox VMs/centos8/Snapshots/{5657ee45-6b16-4138-bbdc-f4e51053d3e7}.vmdk (UUID: 5657ee45-6b16-4138-bbdc-f4e51053d3e7)
        NIC 1:                       MAC: 080027D0B9AE, Attachment: NAT, Cable connected: on, Trace: off (file: none), Type: 82540EM, Reported speed: 0 Mbps, Boot priority: 0, Promisc Policy: deny, Bandwidth group: none
        NIC 1 Settings:  MTU: 0, Socket (send: 64, receive: 64), TCP Window (send:64, receive: 64)
        NIC 1 Rule(0):   name = ssh, protocol = tcp, host ip = 127.0.0.1, host port = 2222, guest ip = , guest port = 22
        NIC 2:                       MAC: 080027DE5034, Attachment: Internal Network 'intnet', Cable connected: on, Trace: off (file: none), Type: 82540EM, Reported speed: 0 Mbps, Boot priority: 0, Promisc Policy: deny, Bandwidth group: none
        NIC 3:                       disabled
        NIC 4:                       disabled
        NIC 5:                       disabled
        NIC 6:                       disabled
        NIC 7:                       disabled
        NIC 8:                       disabled
        Pointing Device:             PS/2 Mouse
        Keyboard Device:             PS/2 Keyboard
        UART 1:                      disabled
        UART 2:                      disabled
        UART 3:                      disabled
        UART 4:                      disabled
        LPT 1:                       disabled
        LPT 2:                       disabled
        Audio:                       disabled
        Audio playback:              disabled
        Audio capture:               disabled
        Clipboard Mode:              Bidirectional
        Drag and drop Mode:          disabled
        Session name:                GUI/Qt
        VRDE:                        enabled (Address 127.0.0.1, Ports 11615, MultiConn: off, ReuseSingleConn: off, Authentication type: null)
        Video redirection:           disabled
        VRDE property               : TCP/Ports  = "11615"
        VRDE property               : TCP/Address = "127.0.0.1"
        VRDE property               : VideoChannel/Enabled = <not set>
        VRDE property               : VideoChannel/Quality = <not set>
        VRDE property               : VideoChannel/DownscaleProtection = <not set>
        VRDE property               : Client/DisableDisplay = <not set>
        VRDE property               : Client/DisableInput = <not set>
        VRDE property               : Client/DisableAudio = <not set>
        VRDE property               : Client/DisableUSB = <not set>
        VRDE property               : Client/DisableClipboard = <not set>
        VRDE property               : Client/DisableUpstreamAudio = <not set>
        VRDE property               : Client/DisableRDPDR = <not set>
        VRDE property               : H3DRedirect/Enabled = <not set>
        VRDE property               : Security/Method = <not set>
        VRDE property               : Security/ServerCertificate = <not set>
        VRDE property               : Security/ServerPrivateKey = <not set>
        VRDE property               : Security/CACertificate = <not set>
        VRDE property               : Audio/RateCorrectionMode = <not set>
        VRDE property               : Audio/LogPath = <not set>
        OHCI USB:                    disabled
        EHCI USB:                    disabled
        xHCI USB:                    disabled
        <BLANKLINE>
        USB Device Filters:
        <BLANKLINE>
        <none>
        <BLANKLINE>
        Bandwidth groups:  <none>
        <BLANKLINE>
        Shared folders:<none>
        <BLANKLINE>
        Capturing:                   not active
        Capture audio:               not active
        Capture screens:             0
        Capture file:                /Users/mfm/VirtualBox VMs/centos8/centos8.webm
        Capture dimensions:          1024x768
        Capture rate:                512kbps
        Capture FPS:                 25kbps
        Capture options:
        <BLANKLINE>
        Guest:
        <BLANKLINE>
        Configured memory balloon size: 0MB
        <BLANKLINE>
        Snapshots:
        <BLANKLINE>
        Name: vagrant up (UUID: 58bae67f-86a0-4b9d-8704-e633ce0e90bc)
        Description:
        220302233336 5937 mfm@Mikes-MacBook-Pro.local:/Users/mfm/vagrant/centos8 <<< vagrant up
        Bringing machine 'default' up with 'virtualbox' provider...
        ==> default: Importing base box 'generic/centos8'...
        ==> default: Matching MAC address for NAT networking...
        ==> default: Setting the name of the VM: centos8
        ==> default: Clearing any previously set network interfaces...
        ==> default: Preparing network interfaces based on configuration...
        default: Adapter 1: nat
        default: Adapter 2: intnet
        ==> default: Forwarding ports...
        default: 22 (guest) => 2222 (host) (adapter 1)
        ==> default: Running 'pre-boot' VM customizations...
        ==> default: Booting VM...
        ==> default: Waiting for machine to boot. This may take a few minutes...
        default: SSH address: 127.0.0.1:2222
        default: SSH username: vagrant
        default: SSH auth method: private key
        default:
        default: Vagrant insecure key detected. Vagrant will automatically replace
        default: this with a newly generated keypair for better security.
        default:
        default: Inserting generated public key within guest...
        default: Removing insecure key from the guest if it's present...
        default: Key inserted! Disconnecting and reconnecting using new SSH key...
        ==> default: Machine booted and ready!
        ==> default: Checking for guest additions in VM...
        ==> default: Setting hostname...
        ==> default: Configuring and enabling network interfaces...
        Name: Converting from CentOS Linux 8 to CentOS Stream 8 (UUID: 4f084f2b-3a27-4496-b33d-2a339f449853)
        Description:
        dnf --disablerepo '*' --enablerepo extras swap centos-linux-repos centos-stream-repos
        dnf distro-sync
        Name: install docker (UUID: 484dbd16-396f-4c09-9444-bdf8ab7c943e) *
        Description:
        #see https://docs.docker.com/engine/install/centos/
        curl -fsSL https://get.docker.com -o get-docker.sh
        DRY_RUN=1 sh ./get-docker.sh
        sudo sh get-docker.sh
        <BLANKLINE>
        <BLANKLINE>
        """
        args = [self.__vbox_path, 'list', 'runningvms']
        if long:
            args.insert(-1, '-l')
        return lib.invoke_subprocess(args)

    def list_ostypes(self):
        """
        >>> for line in MyBox().list_ostypes().split(NL):
        ...     print(line.strip())
        ID:          Other
        Description: Other/Unknown
        Family ID:   Other
        Family Desc: Other
        64 bit:      false
        <BLANKLINE>
        ID:          Other_64
        Description: Other/Unknown (64-bit)
        Family ID:   Other
        Family Desc: Other
        64 bit:      true
        <BLANKLINE>
        ID:          Windows31
        Description: Windows 3.1
        Family ID:   Windows
        Family Desc: Microsoft Windows
        64 bit:      false
        <BLANKLINE>
        ID:          Windows95
        Description: Windows 95
        Family ID:   Windows
        Family Desc: Microsoft Windows
        64 bit:      false
        <BLANKLINE>
        ID:          Windows98
        Description: Windows 98
        Family ID:   Windows
        Family Desc: Microsoft Windows
        64 bit:      false
        <BLANKLINE>
        ID:          WindowsMe
        Description: Windows ME
        Family ID:   Windows
        Family Desc: Microsoft Windows
        64 bit:      false
        <BLANKLINE>
        ID:          WindowsNT3x
        Description: Windows NT 3.x
        Family ID:   Windows
        Family Desc: Microsoft Windows
        64 bit:      false
        <BLANKLINE>
        ID:          WindowsNT4
        Description: Windows NT 4
        Family ID:   Windows
        Family Desc: Microsoft Windows
        64 bit:      false
        <BLANKLINE>
        ID:          Windows2000
        Description: Windows 2000
        Family ID:   Windows
        Family Desc: Microsoft Windows
        64 bit:      false
        <BLANKLINE>
        ID:          WindowsXP
        Description: Windows XP (32-bit)
        Family ID:   Windows
        Family Desc: Microsoft Windows
        64 bit:      false
        <BLANKLINE>
        ID:          WindowsXP_64
        Description: Windows XP (64-bit)
        Family ID:   Windows
        Family Desc: Microsoft Windows
        64 bit:      true
        <BLANKLINE>
        ID:          Windows2003
        Description: Windows 2003 (32-bit)
        Family ID:   Windows
        Family Desc: Microsoft Windows
        64 bit:      false
        <BLANKLINE>
        ID:          Windows2003_64
        Description: Windows 2003 (64-bit)
        Family ID:   Windows
        Family Desc: Microsoft Windows
        64 bit:      true
        <BLANKLINE>
        ID:          WindowsVista
        Description: Windows Vista (32-bit)
        Family ID:   Windows
        Family Desc: Microsoft Windows
        64 bit:      false
        <BLANKLINE>
        ID:          WindowsVista_64
        Description: Windows Vista (64-bit)
        Family ID:   Windows
        Family Desc: Microsoft Windows
        64 bit:      true
        <BLANKLINE>
        ID:          Windows2008
        Description: Windows 2008 (32-bit)
        Family ID:   Windows
        Family Desc: Microsoft Windows
        64 bit:      false
        <BLANKLINE>
        ID:          Windows2008_64
        Description: Windows 2008 (64-bit)
        Family ID:   Windows
        Family Desc: Microsoft Windows
        64 bit:      true
        <BLANKLINE>
        ID:          Windows7
        Description: Windows 7 (32-bit)
        Family ID:   Windows
        Family Desc: Microsoft Windows
        64 bit:      false
        <BLANKLINE>
        ID:          Windows7_64
        Description: Windows 7 (64-bit)
        Family ID:   Windows
        Family Desc: Microsoft Windows
        64 bit:      true
        <BLANKLINE>
        ID:          Windows8
        Description: Windows 8 (32-bit)
        Family ID:   Windows
        Family Desc: Microsoft Windows
        64 bit:      false
        <BLANKLINE>
        ID:          Windows8_64
        Description: Windows 8 (64-bit)
        Family ID:   Windows
        Family Desc: Microsoft Windows
        64 bit:      true
        <BLANKLINE>
        ID:          Windows81
        Description: Windows 8.1 (32-bit)
        Family ID:   Windows
        Family Desc: Microsoft Windows
        64 bit:      false
        <BLANKLINE>
        ID:          Windows81_64
        Description: Windows 8.1 (64-bit)
        Family ID:   Windows
        Family Desc: Microsoft Windows
        64 bit:      true
        <BLANKLINE>
        ID:          Windows2012_64
        Description: Windows 2012 (64-bit)
        Family ID:   Windows
        Family Desc: Microsoft Windows
        64 bit:      true
        <BLANKLINE>
        ID:          Windows10
        Description: Windows 10 (32-bit)
        Family ID:   Windows
        Family Desc: Microsoft Windows
        64 bit:      false
        <BLANKLINE>
        ID:          Windows10_64
        Description: Windows 10 (64-bit)
        Family ID:   Windows
        Family Desc: Microsoft Windows
        64 bit:      true
        <BLANKLINE>
        ID:          Windows2016_64
        Description: Windows 2016 (64-bit)
        Family ID:   Windows
        Family Desc: Microsoft Windows
        64 bit:      true
        <BLANKLINE>
        ID:          Windows2019_64
        Description: Windows 2019 (64-bit)
        Family ID:   Windows
        Family Desc: Microsoft Windows
        64 bit:      true
        <BLANKLINE>
        ID:          Windows11_64
        Description: Windows 11 (64-bit)
        Family ID:   Windows
        Family Desc: Microsoft Windows
        64 bit:      true
        <BLANKLINE>
        ID:          WindowsNT
        Description: Other Windows (32-bit)
        Family ID:   Windows
        Family Desc: Microsoft Windows
        64 bit:      false
        <BLANKLINE>
        ID:          WindowsNT_64
        Description: Other Windows (64-bit)
        Family ID:   Windows
        Family Desc: Microsoft Windows
        64 bit:      true
        <BLANKLINE>
        ID:          Linux22
        Description: Linux 2.2
        Family ID:   Linux
        Family Desc: Linux
        64 bit:      false
        <BLANKLINE>
        ID:          Linux24
        Description: Linux 2.4 (32-bit)
        Family ID:   Linux
        Family Desc: Linux
        64 bit:      false
        <BLANKLINE>
        ID:          Linux24_64
        Description: Linux 2.4 (64-bit)
        Family ID:   Linux
        Family Desc: Linux
        64 bit:      true
        <BLANKLINE>
        ID:          Linux26
        Description: Linux 2.6 / 3.x / 4.x (32-bit)
        Family ID:   Linux
        Family Desc: Linux
        64 bit:      false
        <BLANKLINE>
        ID:          Linux26_64
        Description: Linux 2.6 / 3.x / 4.x (64-bit)
        Family ID:   Linux
        Family Desc: Linux
        64 bit:      true
        <BLANKLINE>
        ID:          ArchLinux
        Description: Arch Linux (32-bit)
        Family ID:   Linux
        Family Desc: Linux
        64 bit:      false
        <BLANKLINE>
        ID:          ArchLinux_64
        Description: Arch Linux (64-bit)
        Family ID:   Linux
        Family Desc: Linux
        64 bit:      true
        <BLANKLINE>
        ID:          Debian
        Description: Debian (32-bit)
        Family ID:   Linux
        Family Desc: Linux
        64 bit:      false
        <BLANKLINE>
        ID:          Debian_64
        Description: Debian (64-bit)
        Family ID:   Linux
        Family Desc: Linux
        64 bit:      true
        <BLANKLINE>
        ID:          Fedora
        Description: Fedora (32-bit)
        Family ID:   Linux
        Family Desc: Linux
        64 bit:      false
        <BLANKLINE>
        ID:          Fedora_64
        Description: Fedora (64-bit)
        Family ID:   Linux
        Family Desc: Linux
        64 bit:      true
        <BLANKLINE>
        ID:          Gentoo
        Description: Gentoo (32-bit)
        Family ID:   Linux
        Family Desc: Linux
        64 bit:      false
        <BLANKLINE>
        ID:          Gentoo_64
        Description: Gentoo (64-bit)
        Family ID:   Linux
        Family Desc: Linux
        64 bit:      true
        <BLANKLINE>
        ID:          Mandriva
        Description: Mandriva (32-bit)
        Family ID:   Linux
        Family Desc: Linux
        64 bit:      false
        <BLANKLINE>
        ID:          Mandriva_64
        Description: Mandriva (64-bit)
        Family ID:   Linux
        Family Desc: Linux
        64 bit:      true
        <BLANKLINE>
        ID:          Oracle
        Description: Oracle (32-bit)
        Family ID:   Linux
        Family Desc: Linux
        64 bit:      false
        <BLANKLINE>
        ID:          Oracle_64
        Description: Oracle (64-bit)
        Family ID:   Linux
        Family Desc: Linux
        64 bit:      true
        <BLANKLINE>
        ID:          RedHat
        Description: Red Hat (32-bit)
        Family ID:   Linux
        Family Desc: Linux
        64 bit:      false
        <BLANKLINE>
        ID:          RedHat_64
        Description: Red Hat (64-bit)
        Family ID:   Linux
        Family Desc: Linux
        64 bit:      true
        <BLANKLINE>
        ID:          OpenSUSE
        Description: openSUSE (32-bit)
        Family ID:   Linux
        Family Desc: Linux
        64 bit:      false
        <BLANKLINE>
        ID:          OpenSUSE_64
        Description: openSUSE (64-bit)
        Family ID:   Linux
        Family Desc: Linux
        64 bit:      true
        <BLANKLINE>
        ID:          Turbolinux
        Description: Turbolinux (32-bit)
        Family ID:   Linux
        Family Desc: Linux
        64 bit:      false
        <BLANKLINE>
        ID:          Turbolinux_64
        Description: Turbolinux (64-bit)
        Family ID:   Linux
        Family Desc: Linux
        64 bit:      true
        <BLANKLINE>
        ID:          Ubuntu
        Description: Ubuntu (32-bit)
        Family ID:   Linux
        Family Desc: Linux
        64 bit:      false
        <BLANKLINE>
        ID:          Ubuntu_64
        Description: Ubuntu (64-bit)
        Family ID:   Linux
        Family Desc: Linux
        64 bit:      true
        <BLANKLINE>
        ID:          Xandros
        Description: Xandros (32-bit)
        Family ID:   Linux
        Family Desc: Linux
        64 bit:      false
        <BLANKLINE>
        ID:          Xandros_64
        Description: Xandros (64-bit)
        Family ID:   Linux
        Family Desc: Linux
        64 bit:      true
        <BLANKLINE>
        ID:          Linux
        Description: Other Linux (32-bit)
        Family ID:   Linux
        Family Desc: Linux
        64 bit:      false
        <BLANKLINE>
        ID:          Linux_64
        Description: Other Linux (64-bit)
        Family ID:   Linux
        Family Desc: Linux
        64 bit:      true
        <BLANKLINE>
        ID:          Solaris
        Description: Oracle Solaris 10 5/09 and earlier (32-bit)
        Family ID:   Solaris
        Family Desc: Solaris
        64 bit:      false
        <BLANKLINE>
        ID:          Solaris_64
        Description: Oracle Solaris 10 5/09 and earlier (64-bit)
        Family ID:   Solaris
        Family Desc: Solaris
        64 bit:      true
        <BLANKLINE>
        ID:          OpenSolaris
        Description: Oracle Solaris 10 10/09 and later (32-bit)
        Family ID:   Solaris
        Family Desc: Solaris
        64 bit:      false
        <BLANKLINE>
        ID:          OpenSolaris_64
        Description: Oracle Solaris 10 10/09 and later (64-bit)
        Family ID:   Solaris
        Family Desc: Solaris
        64 bit:      true
        <BLANKLINE>
        ID:          Solaris11_64
        Description: Oracle Solaris 11 (64-bit)
        Family ID:   Solaris
        Family Desc: Solaris
        64 bit:      true
        <BLANKLINE>
        ID:          FreeBSD
        Description: FreeBSD (32-bit)
        Family ID:   BSD
        Family Desc: BSD
        64 bit:      false
        <BLANKLINE>
        ID:          FreeBSD_64
        Description: FreeBSD (64-bit)
        Family ID:   BSD
        Family Desc: BSD
        64 bit:      true
        <BLANKLINE>
        ID:          OpenBSD
        Description: OpenBSD (32-bit)
        Family ID:   BSD
        Family Desc: BSD
        64 bit:      false
        <BLANKLINE>
        ID:          OpenBSD_64
        Description: OpenBSD (64-bit)
        Family ID:   BSD
        Family Desc: BSD
        64 bit:      true
        <BLANKLINE>
        ID:          NetBSD
        Description: NetBSD (32-bit)
        Family ID:   BSD
        Family Desc: BSD
        64 bit:      false
        <BLANKLINE>
        ID:          NetBSD_64
        Description: NetBSD (64-bit)
        Family ID:   BSD
        Family Desc: BSD
        64 bit:      true
        <BLANKLINE>
        ID:          OS21x
        Description: OS/2 1.x
        Family ID:   OS2
        Family Desc: IBM OS/2
        64 bit:      false
        <BLANKLINE>
        ID:          OS2Warp3
        Description: OS/2 Warp 3
        Family ID:   OS2
        Family Desc: IBM OS/2
        64 bit:      false
        <BLANKLINE>
        ID:          OS2Warp4
        Description: OS/2 Warp 4
        Family ID:   OS2
        Family Desc: IBM OS/2
        64 bit:      false
        <BLANKLINE>
        ID:          OS2Warp45
        Description: OS/2 Warp 4.5
        Family ID:   OS2
        Family Desc: IBM OS/2
        64 bit:      false
        <BLANKLINE>
        ID:          OS2eCS
        Description: eComStation
        Family ID:   OS2
        Family Desc: IBM OS/2
        64 bit:      false
        <BLANKLINE>
        ID:          OS2ArcaOS
        Description: ArcaOS
        Family ID:   OS2
        Family Desc: IBM OS/2
        64 bit:      false
        <BLANKLINE>
        ID:          OS2
        Description: Other OS/2
        Family ID:   OS2
        Family Desc: IBM OS/2
        64 bit:      false
        <BLANKLINE>
        ID:          MacOS
        Description: Mac OS X (32-bit)
        Family ID:   MacOS
        Family Desc: Mac OS X
        64 bit:      false
        <BLANKLINE>
        ID:          MacOS_64
        Description: Mac OS X (64-bit)
        Family ID:   MacOS
        Family Desc: Mac OS X
        64 bit:      true
        <BLANKLINE>
        ID:          MacOS106
        Description: Mac OS X 10.6 Snow Leopard (32-bit)
        Family ID:   MacOS
        Family Desc: Mac OS X
        64 bit:      false
        <BLANKLINE>
        ID:          MacOS106_64
        Description: Mac OS X 10.6 Snow Leopard (64-bit)
        Family ID:   MacOS
        Family Desc: Mac OS X
        64 bit:      true
        <BLANKLINE>
        ID:          MacOS107_64
        Description: Mac OS X 10.7 Lion (64-bit)
        Family ID:   MacOS
        Family Desc: Mac OS X
        64 bit:      true
        <BLANKLINE>
        ID:          MacOS108_64
        Description: Mac OS X 10.8 Mountain Lion (64-bit)
        Family ID:   MacOS
        Family Desc: Mac OS X
        64 bit:      true
        <BLANKLINE>
        ID:          MacOS109_64
        Description: Mac OS X 10.9 Mavericks (64-bit)
        Family ID:   MacOS
        Family Desc: Mac OS X
        64 bit:      true
        <BLANKLINE>
        ID:          MacOS1010_64
        Description: Mac OS X 10.10 Yosemite (64-bit)
        Family ID:   MacOS
        Family Desc: Mac OS X
        64 bit:      true
        <BLANKLINE>
        ID:          MacOS1011_64
        Description: Mac OS X 10.11 El Capitan (64-bit)
        Family ID:   MacOS
        Family Desc: Mac OS X
        64 bit:      true
        <BLANKLINE>
        ID:          MacOS1012_64
        Description: macOS 10.12 Sierra (64-bit)
        Family ID:   MacOS
        Family Desc: Mac OS X
        64 bit:      true
        <BLANKLINE>
        ID:          MacOS1013_64
        Description: macOS 10.13 High Sierra (64-bit)
        Family ID:   MacOS
        Family Desc: Mac OS X
        64 bit:      true
        <BLANKLINE>
        ID:          DOS
        Description: DOS
        Family ID:   Other
        Family Desc: Other
        64 bit:      false
        <BLANKLINE>
        ID:          Netware
        Description: Netware
        Family ID:   Other
        Family Desc: Other
        64 bit:      false
        <BLANKLINE>
        ID:          L4
        Description: L4
        Family ID:   Other
        Family Desc: Other
        64 bit:      false
        <BLANKLINE>
        ID:          QNX
        Description: QNX
        Family ID:   Other
        Family Desc: Other
        64 bit:      false
        <BLANKLINE>
        ID:          JRockitVE
        Description: JRockitVE
        Family ID:   Other
        Family Desc: Other
        64 bit:      false
        <BLANKLINE>
        ID:          VBoxBS_64
        Description: VirtualBox Bootsector Test (64-bit)
        Family ID:   Other
        Family Desc: Other
        64 bit:      true
        <BLANKLINE>
        <BLANKLINE>
        """
        return lib.invoke_subprocess([self.__vbox_path, 'list', 'ostypes'])

    def createvm(self,
                 name,
                 basefolder=pathlib.Path(__file__).parent,
                 ostype="Debian_64",
                 register=True):
        """
        >>> for line in MyBox().createvm(f'createvm{lib.dt_str()}').split(NL):
        ...     print(line.strip())
        Virtual machine 'createvm220406034829727347' is created and registered.
        UUID: 4390100b-b933-46b9-825c-fb6e1f006f8d
        Settings file: '/Users/mfm/my_python/my_vbox/createvm220406034829727347/createvm220406034829727347.vbox'
        <BLANKLINE>
        """
        word_list = [ self.__vbox_path, 'createvm', '--name', name]
        if basefolder is not None:
            word_list.extend(['--basefolder', basefolder])
        if ostype is not None:
            word_list.extend(['--ostype', ostype])
        if register:
            word_list.append('--register')
        return lib.invoke_subprocess(word_list)
