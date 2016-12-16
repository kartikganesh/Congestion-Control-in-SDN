
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpidToStr
from pox.lib.addresses import IPAddr, EthAddr
from pox.lib.packet.arp import arp
from pox.lib.packet.ethernet import ethernet, ETHER_BROADCAST
from pox.lib.packet.packet_base import packet_base
from pox.lib.packet.packet_utils import *
import pox.lib.packet as pkt
from pox.lib.recoco import Timer
import time
 
log = core.getLogger()
 
s1_dpid=0
s2_dpid=0
s3_dpid=0
s4_dpid=0
s5_dpid=0
 
s1_p1=0
s1_p4=0
s1_p5=0
s1_p6=0
s2_p1=0
s3_p1=0
s4_p1=0
 
pre_s1_p1=0
pre_s1_p4=0
pre_s1_p5=0
pre_s1_p6=0
pre_s2_p1=0
pre_s3_p1=0
pre_s4_p1=0


def _handle_portstats_received (event):
  global s1_dpid, s2_dpid, s3_dpid, s4_dpid, s5_dpid
  global s1_p1,s1_p4, s1_p5, s1_p6, s2_p1, s3_p1, s4_p1
  global pre_s1_p1,pre_s1_p4, pre_s1_p5, pre_s1_p6, pre_s2_p1, pre_s3_p1, pre_s4_p1
 
  if event.connection.dpid==s1_dpid:
    for f in event.stats:
      if int(f.port_no)<65534:
        if f.port_no==1:
          pre_s1_p1=s1_p1
          s1_p1=f.rx_packets
          #print "s1_p1->","TxDrop:", f.tx_dropped,"RxDrop:",f.rx_dropped,"TxErr:",f.tx_errors,"CRC:",f.rx_crc_err,"Coll:",f.collisions,"Tx:",f.tx_packets,"Rx:",f.rx_packets
        if f.port_no==4:
          pre_s1_p4=s1_p4
          s1_p4=f.tx_packets
          #s1_p4=f.tx_bytes
          #print "s1_p4->","TxDrop:", f.tx_dropped,"RxDrop:",f.rx_dropped,"TxErr:",f.tx_errors,"CRC:",f.rx_crc_err,"Coll:",f.collisions,"Tx:",f.tx_packets,"Rx:",f.rx_packets
        if f.port_no==5:
          pre_s1_p5=s1_p5
          s1_p5=f.tx_packets
        if f.port_no==6:
          pre_s1_p6=s1_p6
          s1_p6=f.tx_packets
 
  if event.connection.dpid==s2_dpid:
     for f in event.stats:
       if int(f.port_no)<65534:
         if f.port_no==1:
           pre_s2_p1=s2_p1
           s2_p1=f.rx_packets
           #s2_p1=f.rx_bytes
     print getTheTime(), "s1_p4(Sent):", (s1_p4-pre_s1_p4), "s2_p1(Received):", (s2_p1-pre_s2_p1)
 
  if event.connection.dpid==s3_dpid:
     for f in event.stats:
       if int(f.port_no)<65534:
         if f.port_no==1:
           pre_s3_p1=s3_p1
           s3_p1=f.rx_packets
     print getTheTime(), "s1_p5(Sent):", (s1_p5-pre_s1_p5), "s3_p1(Received):", (s3_p1-pre_s3_p1)    
 
  if event.connection.dpid==s4_dpid:
     for f in event.stats:
       if int(f.port_no)<65534:
         if f.port_no==1:
           pre_s4_p1=s4_p1
           s4_p1=f.rx_packets
     print getTheTime(), "s1_p6(Sent):", (s1_p6-pre_s1_p6), "s4_p1(Received):", (s4_p1-pre_s4_p1)  
 
def _handle_ConnectionUp (event):
  global s1_dpid, s2_dpid, s3_dpid, s4_dpid, s5_dpid
  print "ConnectionUp: ",dpidToStr(event.connection.dpid)
 
  #remember the connection dpid for switch
  for m in event.connection.features.ports:
    if m.name == "s1-eth1":
      s1_dpid = event.connection.dpid
      print "s1_dpid=", s1_dpid
      print "installing flow rules s1"
      msg = of.ofp_flow_mod()
      msg.priority =100
      msg.idle_timeout = 0
      msg.hard_timeout = 0
      msg.match.dl_type = 0x0800
      msg.match.nw_dst = "10.0.0.1"
      msg.actions.append(of.ofp_action_output(port = 1))
      event.connection.send(msg)

      msg = of.ofp_flow_mod()
      msg.priority =100
      msg.idle_timeout = 0
      msg.hard_timeout = 0
      msg.match.dl_type = 0x0800
      msg.match.nw_dst = "10.0.0.2"
      msg.actions.append(of.ofp_action_output(port = 2))
      event.connection.send(msg)
 
      msg = of.ofp_flow_mod()
      msg.priority =100
      msg.idle_timeout = 0
      msg.hard_timeout = 0
      msg.match.dl_type = 0x0800
      msg.match.nw_dst = "10.0.0.3"
      msg.actions.append(of.ofp_action_output(port = 3))
      event.connection.send(msg)
 
 #port 5 is path 1
 #send UDP traffic to port 4
 #this is an IP packet
      msg = of.ofp_flow_mod()
      msg.priority =100
      msg.idle_timeout = 0
      msg.hard_timeout = 0
      msg.match.dl_type = 0x0800
      msg.match.nw_proto = 17   #UDP protocol.
      msg.actions.append(of.ofp_action_output(port = 4))
      event.connection.send(msg)  
 
 
 #path 2....
      msg = of.ofp_flow_mod()
      msg.priority =100
      msg.idle_timeout = 0
      msg.hard_timeout = 1
      msg.match.dl_type = 0x0800
      msg.match.nw_proto = 6   #TCP protocol.
      #msg.match.tp_src = 50    #cant specify tcp source on iperf, we use dst for proof of concept
      msg.match.tp_dst = 5001
      msg.actions.append(of.ofp_action_output(port = 5))
      event.connection.send(msg)
 
 
 #path 3, all other 
      msg = of.ofp_flow_mod()
      msg.priority =100
      msg.idle_timeout = 0
      msg.hard_timeout = 0
      msg.match.dl_type = 0x0800
      msg.actions.append(of.ofp_action_output(port = 6))
      event.connection.send(msg)
     
    elif m.name == "s2-eth1":
      s2_dpid = event.connection.dpid
      print "s2_dpid=", s2_dpid
      msg = of.ofp_flow_mod()
      msg.priority =10
      msg.idle_timeout = 0
      msg.hard_timeout = 0
      msg.match.in_port = 1
      msg.match.dl_type=0x0806
      msg.actions.append(of.ofp_action_output(port = 2))
      event.connection.send(msg)
 
      msg = of.ofp_flow_mod()
      msg.priority =10
      msg.idle_timeout = 0
      msg.hard_timeout = 0
      msg.match.in_port = 1
      msg.match.dl_type=0x0800
      msg.actions.append(of.ofp_action_output(port = 2))
      event.connection.send(msg)
  
      msg = of.ofp_flow_mod()
      msg.priority =10
      msg.idle_timeout = 0
      msg.hard_timeout = 0
      msg.match.in_port = 2
      msg.match.dl_type=0x0806
      msg.actions.append(of.ofp_action_output(port = 1))
      event.connection.send(msg)
 
      msg = of.ofp_flow_mod()
      msg.priority =10
      msg.idle_timeout = 0
      msg.hard_timeout = 0
      msg.match.in_port = 2
      msg.match.dl_type=0x0800
      msg.actions.append(of.ofp_action_output(port = 1))
      event.connection.send(msg)
      
    elif m.name == "s3-eth1":
      s3_dpid = event.connection.dpid
      print "s3_dpid=", s3_dpid
    
      msg = of.ofp_flow_mod()
      msg.priority =10
      msg.idle_timeout = 0
      msg.hard_timeout = 0
      msg.match.in_port = 1
      msg.match.dl_type=0x0806
      msg.actions.append(of.ofp_action_output(port = 2))
      event.connection.send(msg)
 
      msg = of.ofp_flow_mod()
      msg.priority =10
      msg.idle_timeout = 0
      msg.hard_timeout = 0
      msg.match.in_port = 1
      msg.match.dl_type=0x0800
      msg.actions.append(of.ofp_action_output(port = 2))
      event.connection.send(msg)
  
      msg = of.ofp_flow_mod()
      msg.priority =10
      msg.idle_timeout = 0
      msg.hard_timeout = 0
      msg.match.in_port = 2
      msg.match.dl_type=0x0806
      msg.actions.append(of.ofp_action_output(port = 1))
      event.connection.send(msg)
  
      msg = of.ofp_flow_mod()
      msg.priority =10
      msg.idle_timeout = 0
      msg.hard_timeout = 0
      msg.match.in_port = 2
      msg.match.dl_type=0x0800
      msg.actions.append(of.ofp_action_output(port = 1))
      event.connection.send(msg)
    
      
      
    elif m.name == "s4-eth1":
      s4_dpid = event.connection.dpid
      print "s4_dpid=", s4_dpid
      msg = of.ofp_flow_mod()
      msg.priority =10
      msg.idle_timeout = 0
      msg.hard_timeout = 0
      msg.match.in_port = 1
      msg.match.dl_type=0x0806
      msg.actions.append(of.ofp_action_output(port = 2))
      event.connection.send(msg)
 
      msg = of.ofp_flow_mod()
      msg.priority =10
      msg.idle_timeout = 0
      msg.hard_timeout = 0
      msg.match.in_port = 1
      msg.match.dl_type=0x0800
      msg.actions.append(of.ofp_action_output(port = 2))
      event.connection.send(msg)
  
      msg = of.ofp_flow_mod()
      msg.priority =10
      msg.idle_timeout = 0
      msg.hard_timeout = 0
      msg.match.in_port = 2
      msg.match.dl_type=0x0806
      msg.actions.append(of.ofp_action_output(port = 1))
      event.connection.send(msg)
 
      msg = of.ofp_flow_mod()
      msg.priority =10
      msg.idle_timeout = 0
      msg.hard_timeout = 0
      msg.match.in_port = 2
      msg.match.dl_type=0x0800
      msg.actions.append(of.ofp_action_output(port = 1))
      event.connection.send(msg)
      
    elif m.name == "s5-eth1":
      s5_dpid = event.connection.dpid
      print "s5_dpid=", s5_dpid
  
      msg = of.ofp_flow_mod()
      msg.priority =100
      msg.idle_timeout = 0
      msg.hard_timeout = 0
      msg.match.dl_type = 0x0800
      msg.match.nw_dst = "10.0.0.1"
      msg.actions.append(of.ofp_action_output(port = 1))
      event.connection.send(msg)
 
      msg = of.ofp_flow_mod()
      msg.priority =10
      msg.idle_timeout = 0
      msg.hard_timeout = 0
      msg.match.in_port = 6
      msg.actions.append(of.ofp_action_output(port = 3))
      event.connection.send(msg)
  
      msg = of.ofp_flow_mod()
      msg.priority =100
      msg.idle_timeout = 0
      msg.hard_timeout = 0
      msg.match.dl_type = 0x0800
      msg.match.nw_dst = "10.0.0.1"
      msg.actions.append(of.ofp_action_output(port = 1))
      event.connection.send(msg)
 
      msg = of.ofp_flow_mod()
      msg.priority =100
      msg.idle_timeout = 0
      msg.hard_timeout = 0
      msg.match.dl_type = 0x0800
      msg.match.nw_dst = "10.0.0.2"
      msg.actions.append(of.ofp_action_output(port = 2))
      event.connection.send(msg)
  
      msg = of.ofp_flow_mod()
      msg.priority =100
      msg.idle_timeout = 0
      msg.hard_timeout = 0
      msg.match.dl_type = 0x0800
      msg.match.nw_dst = "10.0.0.3"
      msg.actions.append(of.ofp_action_output(port = 3))
      event.connection.send(msg)
 
      msg = of.ofp_flow_mod()
      msg.priority =100
      msg.idle_timeout = 0
      msg.hard_timeout = 0
      msg.match.dl_type = 0x0800
      msg.match.nw_dst = "10.0.0.4"
      msg.actions.append(of.ofp_action_output(port = 4))
      event.connection.send(msg)
 
      msg = of.ofp_flow_mod()
      msg.priority =100
      msg.idle_timeout = 0
      msg.hard_timeout = 0
      msg.match.dl_type = 0x0800
      msg.match.nw_dst = "10.0.0.5"
      msg.actions.append(of.ofp_action_output(port = 5))
      event.connection.send(msg)
  
      msg = of.ofp_flow_mod()
      msg.priority =100
      msg.idle_timeout = 0
      msg.hard_timeout = 0
      msg.match.dl_type = 0x0800
      msg.match.nw_dst = "10.0.0.6"
      msg.actions.append(of.ofp_action_output(port = 6))
      event.connection.send(msg)
 
 

 
def _handle_PacketIn(event): #handle arp packets...
  global s1_dpid, s2_dpid, s3_dpid, s4_dpid, s5_dpid
 
  packet=event.parsed
  print "_handle_PacketIn is called, packet.type:", packet.type, " event.connection.dpid:", event.connection.dpid
  if packet.find("udp"):
    print "packet is udp"
  if packet.find("tcp"):
    print "packet is tcp"
#only switch 1 determines the path.
  if event.connection.dpid==s1_dpid:
     a=packet.find('arp')
     if a and a.protodst=="10.0.0.4":
       msg = of.ofp_packet_out(data=event.ofp)
       msg.actions.append(of.ofp_action_output(port=4))
       event.connection.send(msg)
 
     if a and a.protodst=="10.0.0.5":
       msg = of.ofp_packet_out(data=event.ofp)
       msg.actions.append(of.ofp_action_output(port=5))
       event.connection.send(msg)
 
     if a and a.protodst=="10.0.0.6":
       msg = of.ofp_packet_out(data=event.ofp)
       msg.actions.append(of.ofp_action_output(port=6))
       event.connection.send(msg)
 
     if a and a.protodst=="10.0.0.1":
       msg = of.ofp_packet_out(data=event.ofp)
       msg.actions.append(of.ofp_action_output(port=1))
       event.connection.send(msg)
 
     if a and a.protodst=="10.0.0.2":
       msg = of.ofp_packet_out(data=event.ofp)
       msg.actions.append(of.ofp_action_output(port=2))
       event.connection.send(msg)
 
     if a and a.protodst=="10.0.0.3":
       msg = of.ofp_packet_out(data=event.ofp)
       msg.actions.append(of.ofp_action_output(port=3))
       event.connection.send(msg)
  
  
  elif event.connection.dpid==s5_dpid: 
     a=packet.find('arp')
     if a and a.protodst=="10.0.0.4":
       msg = of.ofp_packet_out(data=event.ofp)
       msg.actions.append(of.ofp_action_output(port=4))
       event.connection.send(msg)
 
     if a and a.protodst=="10.0.0.5":
       msg = of.ofp_packet_out(data=event.ofp)
       msg.actions.append(of.ofp_action_output(port=5))
       event.connection.send(msg)
 
     if a and a.protodst=="10.0.0.6":
       msg = of.ofp_packet_out(data=event.ofp)
       msg.actions.append(of.ofp_action_output(port=6))
       event.connection.send(msg)
 
     if a and a.protodst=="10.0.0.1":
       msg = of.ofp_packet_out(data=event.ofp)
       msg.actions.append(of.ofp_action_output(port=1))
       event.connection.send(msg)
 
     if a and a.protodst=="10.0.0.2":
       msg = of.ofp_packet_out(data=event.ofp)
       msg.actions.append(of.ofp_action_output(port=2))
       event.connection.send(msg)
 
     if a and a.protodst=="10.0.0.3":
       msg = of.ofp_packet_out(data=event.ofp)
       msg.actions.append(of.ofp_action_output(port=3))
       event.connection.send(msg)
 
 

def testListener (event):
  packet = event.parsed
  if packet.find("udp"):
    log.debug("udp found: %s:%s to %s:%s", packet.find("ipv4").srcip, packet.find("udp").srcport, packet.find("ipv4").dstip, packet.find("udp").dstport)
    srcTcpPort =  packet.find("udp").srcport 
    dstTcpPort =  packet.find("udp").dstport
  elif packet.find("tcp"):
    log.debug("tcp found: %s:%s to %s:%s", packet.find("ipv4").srcip, packet.find("tcp").srcport, packet.find("ipv4").dstip, packet.find("tcp").dstport)
    srcTcpPort =  packet.find("tcp").srcport 
    dstTcpPort =  packet.find("tcp").dstport
    print "there was an connection (event)"
 
def launch ():
  global start_time
  core.openflow.addListenerByName("PortStatsReceived",_handle_portstats_received)
  core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
  core.openflow.addListenerByName("PacketIn",_handle_PacketIn)
  core.openflow.addListenerByName("PacketIn",testListener)