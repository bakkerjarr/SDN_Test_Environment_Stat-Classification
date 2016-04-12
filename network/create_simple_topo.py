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
        k = 2
        switch_opts = {"inband": False, "protocols": "OpenFlow13"}
        switch = self.addSwitch("s1", opts=switch_opts)
        for i in range(1, k+1):
            host = self.addHost("h{0}".format(i),ip="192.168.56.1{"
                                                    "0}/24".format(i),
                                mac="00:00:00:00:00:0{0}".format(i))
            self.addLink(host, switch)


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
