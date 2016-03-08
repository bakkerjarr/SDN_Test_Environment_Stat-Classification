# SDN_Test_Environment_Stat-Classification

This repository contains programs and scripts for building a small testing environment involving two virtual machines (VMs) and a Mininet network. This means that Mininet can be used to emulate a network topology on a VM (say VM1) and another VM (say VM2) can externally prcoess data mined from the Mininet network.

## Test Environment

Oracle VirtualBox is used to run two VMs created using the SDN Hub 
all-in-one SDN app development starter VM (http://yuba.stanford
.edu/~srini/tutorial/SDN_tutorial_VM_64bit.ova) (available March 8, 
2016).

The following versions of software were used:
    - Mininet 2.2.1
    - Ryu 3.22
    - Open vSwitch 2.3.90

## Establishing Network Connectivity Between VM1 and VM2

1. Create a host-only network in VirtualBox. Initialise with the below
 settings.

    Adapter:
        - IPv4 Address: 192.168.56.1
        - IPv4 Network Mask: 255.255.255.0
        - IPv6 Address: (leave blank)
        - IPv6 Network Mask Length: 0
    
    DHCP Server: leave disabled.

2. Create two VMs (VM1 and VM2) using the VM image mentioned above.

3. For each VM created go to Settings -> Network to configure the network adapters. Ensure that the MAC addresses of all created adapters are different.

    Adapter 1:
        - Attached to: NAT
    
    Adapter 2:
        - Attached to: Host-only Adapter
        - Name: vboxnet0
    
4. Start VM1 and VM2.

5. Within VM1 edit the file /etc/network/interfaces and add the below configuration.

    auto eth1
    iface eth1 inet static
        address 192.168.56.101
        netmask 255.255.255.0
        network 192.168.56.0
        broadcast 192.168.56.255

6. Within VM2 edit the file /etc/network/interfaces and add the below configuration.

    auto eth1
    iface eth1 inet static
        address 192.168.56.102
        netmask 255.255.255.0
        network 192.168.56.0
        broadcast 192.168.56.255

7. Reboot each VM or bring up the eth1 interface using other means.

8. Confirm that eth1 has initialised itself on each VM by using ifconfig.

9. Execute the route command in each VM, the outputted tables should contain the three entries displayed below.

| Destination  | Gateway  | Genmask       | Flags | Metric | Ref | Use | Iface |
|:------------ |:-------- |:------------- |:----- |:------ |:--- | ---:|:----- |
| default      | 10.0.2.2 | 0.0.0.0       | UG    | 0      | 0   | 0   | eth0  |
| 10.0.2.0     | *        | 255.255.255.0 | U     | 0      | 0   | 0   | eth0  |
| 192.168.56.0 | *        | 255.255.255.0 | U     | 0      | 0   | 0   | eth1  |

10. Ping VM2 from VM1 and vice versa to verify that each virtual 
machine can indeed reach one another.

## Commands for Checking Component Versions
Check Mininet version:
    $ mn --version

Check Ryu version:
    $ ~/ryu/bin/ryu-manager --version

Check Open vSwitch version:
    $ ovs-vswitchd --version