#!/bin/bash
#enqueue:port:queue
#funny (or not?) using -OOpenFlow13 results in 'action drop'
#setQueue should be used instead?

#video server switch

sudo ovs-ofctl add-flow vs_sw ip,in_port=1,nw_dst=10.0.0.1,actions=enqueue:2:1
sudo ovs-ofctl add-flow vs_sw ip,in_port=1,nw_dst=10.0.0.2,actions=enqueue:2:2
sudo ovs-ofctl add-flow vs_sw ip,in_port=1,nw_dst=10.0.0.3,actions=enqueue:2:3

sudo ovs-ofctl add-flow vs_sw in_port=2,actions=output:1

#home gateway switch

sudo ovs-ofctl add-flow hgw_sw in_port=1,actions=output:4
sudo ovs-ofctl add-flow hgw_sw in_port=2,actions=output:4
sudo ovs-ofctl add-flow hgw_sw in_port=3,actions=output:4

sudo ovs-ofctl add-flow hgw_sw ip,in_port=4,nw_dst=10.0.0.1,actions=output:1
sudo ovs-ofctl add-flow hgw_sw ip,in_port=4,nw_dst=10.0.0.2,actions=output:2
sudo ovs-ofctl add-flow hgw_sw ip,in_port=4,nw_dst=10.0.0.3,actions=output:3