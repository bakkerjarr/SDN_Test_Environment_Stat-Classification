# SDN_Test_Environment_Stat-Classification

This repository contains programs and scripts for building a small 
testing environment involving two virtual machines (VMs) and a Mininet
network. This means that Mininet can be used to emulate a network
topology on a VM (say VM1) and another VM (say VM2) can externally
prcoess data mined from the Mininet network.

## Test Environment

Oracle VirtualBox is used to run two VMs created using the SDN Hub 
all-in-one SDN app development starter VM. This image can be 
downloaded from http://yuba.stanford.edu/~srini/tutorial/SDN_tutorial_VM_64bit.ova (available March 8, 2016).

The following versions of software were used:
- Mininet 2.2.1
- Ryu 3.22
- Open vSwitch 2.3.90

## Establishing Network Connectivity Between VM1 and VM2 through Mininet

### Step 1. VirtualBox Network Settings

#### VM1
- Adapter 2
⋅⋅- Attached to:  Internal Network vm1->vm2.
⋅⋅- Promiscuous Mode: Allow VMs.
- Adapter 3
⋅⋅- Attached to:  Internal Network vm1->vm1.
⋅⋅- Promiscuous Mode: Allow VMs.
- Adapter 4
⋅⋅- Attached to:  Internal Network vm1->vm1.

#### VM2
- Adapter 2
⋅⋅- Attached to:  Internal Network vm1->vm2.

### Step 2. Virtual Machine Network Configuration
For each VM open and edit /etc/network/interfaces to 
match the configuration below. Reboot each machine once the changes 
have been made.

#### VM1
```
auto eth1
iface eth1 inet manual

auto eth2
iface eth2 inet manual

auto eth3
iface eth3 inet static
    address 192.168.56.101
    netmask 255.255.255.0
    network 192.168.56.0
    broadcast 192.168.56.255
```

#### VM2
```
auto eth1
iface eth1 inet static
    address 192.168.56.102
    netmask 255.255.255.0
    network 192.168.56.0
    broadcast 192.168.56.255
```

### Step 3. Virtual Machine Routing Tables
Log into each each VM and execute the route command. Ensure that the 
entries match those in the route tables below.

#### VM1

| Destination  | Gateway  | Genmask       | Flags | Metric | Ref | Use | Iface |
|:------------ |:-------- |:------------- |:----- |:------ |:--- | ---:|:----- |
| default      | 10.0.2.2 | 0.0.0.0       | UG    | 0      | 0   | 0   | eth0  |
| 10.0.2.0     | *        | 255.255.255.0 | U     | 0      | 0   | 0   | eth0  |
| 192.168.56.0 | *        | 255.255.255.0 | U     | 0      | 0   | 0   | eth3  |

#### VM2

| Destination  | Gateway  | Genmask       | Flags | Metric | Ref | Use | Iface |
|:------------ |:-------- |:------------- |:----- |:------ |:--- | ---:|:----- |
| default      | 10.0.2.2 | 0.0.0.0       | UG    | 0      | 0   | 0   | eth0  |
| 10.0.2.0     | *        | 255.255.255.0 | U     | 0      | 0   | 0   | eth0  |
| 192.168.56.0 | *        | 255.255.255.0 | U     | 0      | 0   | 0   | eth1  |

## Commands for Checking Component Versions
Check Mininet version:
    $ mn --version

Check Ryu version:
    $ ~/ryu/bin/ryu-manager --version

Check Open vSwitch version:
    $ ovs-vswitchd --version