#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scapy.all import *

ap_list = []

def PacketHandler(pkt):
    if pkt.haslayer(Dot11):
        if pkt.addr2 not in ap_list:
            ap_list.append(pkt.addr2)
            print "SENDER MAC: {0} RECIPIEN SSID: {1}".format(pkt.addr2, pkt.addr1)


sniff(iface="mon0", prn = PacketHandler)
