#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scapy.all import *

ap_list = []

def PacketHandler(pkt):
    if pkt.haslayer(Dot11):
        if pkt.addr2 not in ap_list:
            ap_list.append(pkt.addr2)
            print "AP MAC: {0} with SSID:".format(pkt.summary())


sniff(iface="mon0", prn = PacketHandler)
