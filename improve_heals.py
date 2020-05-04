from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.topology import event, switches
from ryu.topology.api import get_switch, get_link, get_host
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
import copy
import networkx as nx
import matplotlib.pyplot as plt
import requests
import json
import random 
from ryu.lib.packet import arp
from ryu.lib.packet import ipv4
from ryu.lib.packet import icmp
from ryu.lib.packet import tcp


with open("proxy_arp.json", 'r') as f:
    proxy_arp = json.load(f)
    f.close()

class SelfHeal13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SelfHeal13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.switch_list = []
        self.link_list = []
        self.list_link = [] 
        self.arp_list = []
        self.broken_list = []  
        self.topo = nx.Graph()

    @set_ev_cls(event.EventSwitchEnter)
    def get_topology(self,ev):
        self.switch_list = get_switch(self,None)
        switches=[switch.dp.id for switch in self.switch_list]
        r  = requests.get(url = "http://192.168.31.5:8080/v1.0/topology/links")
        link_list  = r.json()
        print("Check #############################")
        print(link_list)
        print("Getting into Link List")
        links=[( int(link['src']['dpid'].lstrip('0')), int(link['dst']['dpid'].lstrip('0')), {'out': int(link['src']['port_no'].lstrip('0')), 'in': int(link['dst']['port_no'].lstrip('0')) } ) for link in link_list]
        self.list_link = links 
        print("Switches and Links ################## Topology ")
        print(switches)
        print(links)
        self.topo.add_nodes_from(switches)
        self.topo.add_edges_from(links)
        print("Nodes and Edges ############ Networkx")
        print(self.topo.nodes())
        print(self.topo.edges())

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):

        if ev.msg.msg_len < ev.msg.total_len:
                   self.logger.debug("packet truncated: only %s of %s bytes",
                                           ev.msg.msg_len, ev.msg.total_len)

        msg = ev.msg 
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]
        if eth.ethertype != ether_types.ETH_TYPE_LLDP:
                         
#                print("Message")
#                print(msg)
                print("##################################################################################################################################################################################")
                print("Datapath")
                print(datapath.id)
#                print("Negotiated Protocol")
#                print(ofproto)
#                print("Parser")
#                print(parser)
                print("in_port")
                print("Message Match ")
                print(msg.match)
                print(in_port)
#                print("Message Data")
#                print(msg.data)
                print("Packet")
                print(pkt)
                print("Packet Type")
                print(type(pkt))
                print("Eth")
                print(eth)
                 
                if(pkt.get_protocols(arp.arp)):
                     print("This is an ARP Message")
                     pkt_arp = pkt.get_protocols(arp.arp)[0]
                     arp_dst_ip = pkt_arp.dst_ip
                     arp_src_ip = pkt_arp.src_ip
                     arp_hlen = pkt_arp.hlen
                     arp_hwtype = pkt_arp.hwtype
                     arp_plen = pkt_arp.plen
                     arp_proto = pkt_arp.proto
                     arp_opcode = pkt_arp.opcode
                     arp_src_mac = pkt_arp.src_mac
                     if(eth.src not in self.topo.nodes()):
                         self.topo.add_node(eth.src, ip = arp_src_ip)
                         print("Chec############")
                         self.arp_list.append(self.topo.node[eth.src]['ip'])
                         self.topo.add_edge(datapath.id, eth.src)
                         self.list_link.append((datapath.id, eth.src,{'out' : in_port }))
                     print("Destined for ARP")
                     print(arp_dst_ip)
                     print(self.topo.nodes())
                     print(self.topo.edges())
                     print(self.list_link) 
          
                     if(eth.dst not in self.topo.nodes()): 
                            out_port = ofproto.OFPP_FLOOD
                            actions_arp = [parser.OFPActionOutput(out_port)]
                            match_arp = parser.OFPMatch(in_port=in_port, eth_type=eth.ethertype, eth_dst=eth.dst, eth_src=eth.src)
                            ipInst_arp = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions_arp)]
                            cookie_arp = random.randint(0, 0xffffffffffffffff)
                            flowMod_arp = parser.OFPFlowMod(datapath=datapath,match=match_arp,hard_timeout=3,instructions=ipInst_arp,cookie=cookie_arp)
                            datapath.send_msg(flowMod_arp)
                     
                if((pkt.get_protocols(arp.arp)) or (pkt.get_protocols(ipv4.ipv4))):
                     if((eth.dst in self.topo.nodes()) and (eth.src in self.topo.nodes())): 
                             print("Calculate Shortest Path on the Fly") 
                             sp = nx.shortest_path(self.topo, source = eth.src, target = eth.dst)
                             print(sp)
                             if(datapath.id in sp):
                                 tem = sp[sp.index(datapath.id) + 1] 
                                 sd = [(k[0],k[1]) for k in self.list_link]
                                 temp = sd.index((datapath.id,tem))
				 out_port = self.list_link[temp][2]['out']
				 print("We are going to add flows ")
				 print("From " + str(datapath.id) + " To " + str(tem) + " Through " + str(out_port))
				 actions = [parser.OFPActionOutput(out_port)]
				 match = parser.OFPMatch(in_port=in_port, eth_dst=eth.dst, eth_src=eth.src)
#				 match = parser.OFPMatch(in_port=in_port, eth_type=eth.ethertype,  eth_dst=eth.dst, eth_src=eth.src)
				 ipInst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
				 cookie = random.randint(0, 0xffffffffffffffff)
				 flowMod = parser.OFPFlowMod(datapath=datapath, priority = 100, match=match,idle_timeout=10,instructions=ipInst,cookie=cookie)
				 datapath.send_msg(flowMod)



    @set_ev_cls(ofp_event.EventOFPPortStatus, MAIN_DISPATCHER)
    def port_state_change_handler(self, ev):

               print("Port CHange Status Alert !!!!!!!! ##############################################################################################################################")
               msg = ev.msg
               print(msg)
               dp = msg.datapath
               ofp = dp.ofproto
               ofp_parser = dp.ofproto_parser
               state = msg.desc.state
               change_port = msg.desc.port_no
               print("Datapath ID") 
               print(dp.id)
               print("Port Changed") 
               print(change_port)
               print("Port State CHange") 
               print(state)
               for i in self.list_link: 
                            if((i[0] == dp.id) and (i[2]['out'] == change_port)):
                                  if(state == 1):
                                        if((i[0],i[1]) in self.topo.edges()):
                                             self.topo.remove_edge(i[0],i[1]) 
                                        if((i[1],i[0]) in self.topo.edges()):
                                             self.topo.remove_edge(i[1],i[0]) 

                                  if(state == 0):
                                              self.topo.add_edge(i[0],i[1])

               print("Updating Topology") 
               print(self.topo.nodes())
               print(self.topo.edges())          
               
