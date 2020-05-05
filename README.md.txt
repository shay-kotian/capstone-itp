Traditional Networking couples the Control Plane and the Data Plane often leads to vendor-locking, scalability issues and hinder innovation. Software-Defined Networking facilitates the separation of the Control Plane and the Forwarding Plane of Network Devices. This gives the Network Engineers the power to code the network intelligence in the Control Plane  required for better and efficient packet forwarding in the Forwarding Plane. 
This project studied the present limitations of the Traditional Routing Protocols in a Data Center environment. The Project developed the network intelligence to overcome some of these limitations and improve efficiency. 
Scripts: 

1. functionrest.py : A modular function that enables the network programmer to perform REST, a popular Northbound Protocol, to the SDN Controller 
2. gui-topology.py: An independent function that fetches the complete Network Topology from the SDN Controller and displays the Network Topology in a GUI form in a Browser 
3. improve_heals.py: A modular function that keeps track of the active links and nodes in the topology managed by the SDN controller and calculates the Shortest Path at a given time for a source-destination pair. 
4. linkred.mn: A dynamic Infrastructure as Code (IaC) script to emulate the topology managed by the SDN Controller 
5. nodered.mn: A Infrastructure as a Code (IaC) script to induce controlled faults in the system for stress testing. 
6. linkred.py : A input function fed with linkedred.mn for easy reuse in multiple development environment 
7. nodered.py: A input function fed with nodered.mn for easy reuse in multiple development environment 
8. nat.py: A modular function to enable internal networks to access the Public Internet for Repository updates 
9. ofctl_rest.py: A modular function run on the SDN Controller to allow it to listen for REST calls. 
10. rest_topology.py: A modular function that uses the LLDP protocol to identify active links for new host discovery
11. proxy_arp.json: A json file that is maintained by the SDN controller for proxy arp IP-MAC mapping. 

