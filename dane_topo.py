#!/usr/bin/python


from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel, info, debug
from mininet.node import Host, RemoteController
from mininet.node import Switch
from mininet.nodelib import LinuxBridge

from netaddr import *  #sudo pip install netaddr

import sys





class IperfSinkHost(Host):
    def __init__(self, name, ip, mac, remoteIP, remoteMAC, iperfPort, *args, **kwargs):
        Host.__init__(self, name, ip=ip, mac=mac, *args, **kwargs)

        self.remoteIP = remoteIP
        self.remoteMAC = remoteMAC
        self.iperfPort = iperfPort

    def config(self, **kwargs):
        Host.config(self, **kwargs)

        debug("configuring arp for %s %s" % (self.remoteIP, self.remoteMAC))

        self.setARP(self.remoteIP, self.remoteMAC)
        self.cmd('iperf -s -D -u -p %s' % (self.iperfPort))

#class IperfSourceHost(Host):
#    def __init__(self, name, ip, mac, remoteConfig, *args, **kwargs):
#        Host.__init__(self, name, ip=ip, mac=mac, *args, **kwargs)
#
#        self.remoteConfig = remoteConfig#
#    def config(self, **kwargs):
#        Host.config(self, **kwargs)
#
#        for attrs in self.remoteConfig.itervalues():
#            self.setARP(attrs['remoteIP'], attrs['remoteMAC'])


class IperfSourceHost(Host):
    def __init__(self, name, ip, mac, nHosts, *args, **kwargs):
        Host.__init__(self, name, ip=ip, mac=mac, *args, **kwargs)

        self.nHosts = nHosts

    def config(self, **kwargs):
        Host.config(self, **kwargs)

        for j in range(1, self.nHosts + 1):
            self.setARP('10.0.0.%s' % j, '00:10:00:00:00:0%s' % j)


class daneTopo(Topo):

    def build(self):

        vs_sw = self.addSwitch('vs_sw', dpid='0000000000000001') #video server switch
        hgw_sw = self.addSwitch('hgw_sw', dpid='0000000000000002') #home gateway

        nHosts = 3
        nVideoServers = 1
        vsIP='10.0.0.254'
        vsMAC='00:10:00:00:02:54'
        iperfPortBase=5000


        for j in range(1, nHosts + 1):
            host = self.addHost('h%s' %j, cls=IperfSinkHost, ip='10.0.0.%s/24' %j, mac='00:10:00:00:00:0%s' %j,
                                remoteIP=vsIP, remoteMAC=vsMAC, iperfPort = str(iperfPortBase + j))
            self.addLink(host, hgw_sw)

        vs = self.addHost('vs', cls=IperfSourceHost, ip='%s/24' %vsIP, mac=vsMAC,nHosts = nHosts)
        self.addLink(vs_sw, vs)

        self.addLink(vs_sw,hgw_sw)

#topos = {'tnonorth': MDCoCoTopoNorth,
#         'tnosouth': MDCoCoTopoSouth}


if __name__ == '__main__':
    setLogLevel('debug')
    topo = daneTopo()
    net = Mininet(topo=topo, controller=RemoteController)

    net.start()

    CLI(net)

    net.stop()

    info("done\n")


# topos = { 'cocotopo': ( lambda: CoCoTopo() ) }