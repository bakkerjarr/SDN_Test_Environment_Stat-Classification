#!/usr/bin/env python

import argparse
from mininet.cli import CLI
from mininet.log import lg
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.link import Intf
from mininet.node import OVSSwitch
from mininet.node import RemoteController
from mininet.topo import Topo
from mininet.util import dumpNodeConnections

__author__ = "Jarrod N. Bakker"
__status__ = "Development"


class SimpleTopo(Topo):
    """Network topology consisting of a single switch, controller and
    two hosts.
    """

    def build(self):
        """Build the topology.
        """
        k = 3
        switch_opts = {"inband": False, "protocols": "OpenFlow13"}
        switch = self.addSwitch("s1", opts=switch_opts)
        for i in range(1, k+1):
            host = self.addHost("h{0}".format(i),ip="10.0.0.1{"
                                                    "0}/24".format(i),
                                mac="00:00:00:00:00:0{0}".format(i))
            self.addLink(host, switch)


def set_qos(switch):
    """Set the QoS parameters on a switch.

    :param switch: The switch to operate on.
    """
    lg.info("***Attempting to set QoS parameters on switch {"
            "0}. Output shown below.\n".format(switch.name))
    lg.info(switch.vsctl("clear Port s1-eth2 qos"))
    lg.info(switch.vsctl("--all destroy qos"))
    lg.info(switch.vsctl("-- set Port s1-eth2 qos=@newqos -- "
                         "--id=@newqos create QoS type=linux-htb "
                         "other-config:max-rate=1000000000 queues=0=@q0,"
                         "1=@q1 -- --id=@q0 create Queue "
                         "other-config:max-rate=1000000000 -- --id=@q1 "
                         "create Queue other-config:max-rate=100000"))

def start_mininet(iface_names):
    """Start Mininet with the above topology.

    :param iface_name: Network interface name of the host computer to
    attach to the Mininet virtual network.
    """
    topo = SimpleTopo()
    net = Mininet(topo, build=False)
    net.addController("c0", controller=RemoteController, port=6633,
                      switch=OVSSwitch)
    net.build()
    switch = net.switches[0]
    for iface in iface_names:
        lg.info("***Connecting {0} to virtual switch\n".format(iface))
        # Connect the switch to the eth1 interface of this host machine!
        Intf(iface, node=switch)
    net.start()
    set_qos(switch)
    lg.info("***Dumping host connections\n")
    dumpNodeConnections(net.hosts)
    lg.info("***Dumping switch connections\n")
    dumpNodeConnections(net.switches)
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    ifaces_help = "A list of network interfaces."
    parser = argparse.ArgumentParser(description="Create a Mininet "
                                                 "topology that can "
                                                 "insert the host "
                                                 "machine's network "
                                                 "interfaces into an "
                                                 "OVS instance.")
    parser.add_argument("ifaces", metavar="ifaces", type=str, nargs="+",
                        help=ifaces_help)
    args = parser.parse_args()
    start_mininet(args.ifaces)
