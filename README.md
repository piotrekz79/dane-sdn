1. Allow ODL to use active Connection to OVS Hosts

source: http://docs.opendaylight.org/en/stable-boron/user-guide/ovsdb-netvirt.html

An active connection is when the OVSDB Southbound Plugin initiates the connection to an OVS host. This happens when the OVS host is configured to listen for the connection (i.e. the OVSDB Southbound Plugin is active the the OVS host is passive). The OVS host is configured with the following command:

sudo ovs-vsctl set-manager ptcp:6640

or use 

./init.sh

2. Mininet

cd dane-sdn

Start mininet to create topology

./mnd.sh

In mininet console (prompt: mininet>) open video 3 server terminals, one for each video client

xterm vs vs vs

In these consoles traffic towards clients can be sent using (will not work until configuration is complete)

./vs_h1.sh
./vs_h2.sh
./vs_h3.sh


Next, in regular linux console add flows

./flows

3. configure ODL to communicate with the OVSDB (host DANE1)

POST http://{{CONTROLLER-IP}}:8181/restconf/config/network-topology:network-topology/topology/ovsdb:1/


        {
            "node": [
                {
                    "node-id": "ovsdb:DANE1",
                    "connection-info": {
                        "ovsdb:remote-ip": "{{HYPERVISOR-IP}}",
                        "ovsdb:remote-port": "{{HYPERVISOR-OVSDB-PORT}}"
                    }
                }
            ]
        }

4. If we use mininet to create switch, we do not need to add switch in ODL or create termination point - thery should be present, e.g., for vs_sw switch

GET http://{{CONTROLLER-IP}}:8181/restconf/operational/network-topology:network-topology/topology/ovsdb:1/node/ovsdb:DANE1%2Fbridge%2Fvs_sw/


however, we need to create extra IDs

PUT http://{{CONTROLLER-IP}}:8181/restconf/config/network-topology:network-topology/topology/ovsdb:1/node/ovsdb:DANE1%2Fbridge%2Fvs_sw/termination-point/vs_sw-eth2/

{
  "network-topology:termination-point": [
    {
      "ovsdb:name": "vs_sw-eth2",
      "tp-id": "vs_sw-eth2"
    }
  ]
}






5. Add a QoS entry to a qos-entries list

PUT

http://{{CONTROLLER-IP}}:8181/restconf/config/network-topology:network-topology/topology/ovsdb:1/node/ovsdb:DANE1/ovsdb:qos-entries/DANE-QOS-1/

{
  "ovsdb:qos-entries": [
    {
      "qos-id": "DANE-QOS-1",
      "qos-type": "ovsdb:qos-type-linux-htb"
    }
  ]
}


6. Add a Queue entry to the queues list of a ovsdb node 'DANE1'

PUT http://{{CONTROLLER-IP}}:8181/restconf/config/network-topology:network-topology/topology/ovsdb:1/node/ovsdb:DANE1/ovsdb:queues/DANE-QUEUE-1/

{
  "ovsdb:queues": [
    {
      "queue-id": "DANE-QUEUE-1"
    }
  ]
}

7. Add existing Queue ID entry to a QoS entry

PUT http://{{CONTROLLER-IP}}:8181/restconf/config/network-topology:network-topology/topology/ovsdb:1/node/ovsdb:DANE1/ovsdb:qos-entries/DANE-QOS-1/

{
    "ovsdb:qos-entries": [
        {
            "qos-id": "DANE-QOS-1",
            "queue-list": [
                {
                    "queue-number": "0",
                    "queue-ref": "/network-topology:network-topology/network-topology:topology[network-topology:topology-id='ovsdb:1']/network-topology:node[network-topology:node-id='ovsdb:DANE-HOST1']/ovsdb:queues[ovsdb:queue-id='DANE-QUEUE-1']"
                }
            ]
        }
    ]
}



8. Add existing QoS ID to a termination point

PUT http://{{CONTROLLER-IP}}:8181/restconf/config/network-topology:network-topology/topology/ovsdb:1/node/ovsdb:DANE1%2Fbridge%2Fvs_sw/termination-point/vs_sw-eth2/

{
  "network-topology:termination-point": [
    	{
 	  		"ovsdb:name": "vs_sw-eth2",
 			"tp-id": "vs_sw-eth2",
 			"ovsdb:qos-entry": [
                {
                    "qos-key": 1,
                    "qos-ref": "/network-topology:network-topology/network-topology:topology[network-topology:topology-id='ovsdb:1']/network-topology:node[network-topology:node-id='ovsdb:DANE1']/ovsdb:qos-entries[ovsdb:qos-id='DANE-QOS-1']"
                }
            ]
  		}
    ]
}

9. (Re) configure Queue



PUT http://{{CONTROLLER-IP}}:8181/restconf/config/network-topology:network-topology/topology/ovsdb:1/node/ovsdb:DANE1/ovsdb:queues/DANE-QUEUE-1/


{
  "ovsdb:queues": [
    {
      "queue-id": "DANE-QUEUE-1",
      "queues-other-config": [
        {
          "queue-other-config-key": "max-rate",
          "queue-other-config-value": "7200000"
        }
      ]
    }
  ]
}


10. To add another queue to the same QoS group

first create a queue 

PUT http://{{CONTROLLER-IP}}:8181/restconf/config/network-topology:network-topology/topology/ovsdb:1/node/ovsdb:DANE1/ovsdb:queues/DANE-QUEUE-2/


{
  "ovsdb:queues": [
    {
      "queue-id": "DANE-QUEUE-2",
      "queues-other-config": [
        {
          "queue-other-config-key": "max-rate",
          "queue-other-config-value": "10000000"
        }
      ]
    }
  ]
}




but then only POST to QoS (if we do PUT like in 7. we will delete previous queue)



POST http://{{CONTROLLER-IP}}:8181/restconf/config/network-topology:network-topology/topology/ovsdb:1/node/ovsdb:DANE1/ovsdb:qos-entries/DANE-QOS-1/

{
            "queue-list": [
                {
                    "queue-number": "2",
                    "queue-ref": "/network-topology:network-topology/network-topology:topology[network-topology:topology-id='ovsdb:1']/network-topology:node[network-topology:node-id='ovsdb:DANE-HOST1']/ovsdb:queues[ovsdb:queue-id='DANE-QUEUE-2']"
                }
            ]
}
