#!/bin/bash
#title          :start_network.sh
#description    :Create a network topology in Mininet
#author         :Jarrod N. Bakker
#date           :14/04/2016
#usage          :bash start_network.sh
#========================================================================
clear ;
# Ensure that Mininet is not currently running a network.
sudo mn -c ;

# The below command may be needed in some instances to set the protocol
# to OpenFlow 1.3.
# sudo ovs-vsctl set bridge s1 protocols=OpenFlow13

# Start Mininet with a simple topology of a single OpenFlow switch with
# 2 virtual hosts connected to it along with some of the host's NICs.
echo
echo
sudo python network/create_simple_topo.py enp0s9
