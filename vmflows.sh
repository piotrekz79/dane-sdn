#!/bin/bash
#configuration of home gateway switch ad video server switch

sudo ovs-vsctl add-port hgw_sw ens192 -- set Interface ens192 ofport_request=2

#[PZ] I don't get it :/ bridged iface should accept frames with any MAC but only after the command below we see the traffic passing :/
#..or maybe it does not work like this for ovs but only brctl
sudo ifconfig ens192 hw ether 00:10:00:00:02:54


#video server switch
#sudo ovs-ofctl add-flow vs_sw ip,nw_dst=10.0.0.1,actions=output:2

#enqueue:port:queue
sudo ovs-ofctl add-flow vs_sw ip,in_port=1,nw_dst=10.0.0.1,actions=enqueue:2:1
sudo ovs-ofctl add-flow vs_sw ip,in_port=1,nw_dst=10.0.0.2,actions=enqueue:2:2
sudo ovs-ofctl add-flow vs_sw ip,in_port=1,nw_dst=10.0.0.3,actions=enqueue:2:3

sudo ovs-ofctl add-flow vs_sw in_port=2,actions=output:1

#home gateway switch
sudo ovs-ofctl add-flow hgw_sw ip,nw_dst=10.0.0.1,action=NORMAL
sudo ovs-ofctl add-flow hgw_sw ip,nw_dst=10.0.0.2,action=NORMAL
sudo ovs-ofctl add-flow hgw_sw ip,nw_dst=10.0.0.3,action=NORMAL

sudo ovs-ofctl add-flow hgw_sw ip,nw_dst=10.0.0.254,action=output:1









sudo ovs-ofctl add-flow br-dane ip,nw_dst=10.0.0.1,actions=enqueue:1:2

