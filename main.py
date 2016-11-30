#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scapy.all import *

ap_list = []

def PacketHandler(pkt):
    if pkt.haslayer(Dot11):
        if pkt.addr2 not in ap_list:
            print "SRC MAC: {0} DST MAC: {1}".format(dir(pkt), pkt.addr2)


sniff(iface="mon0", prn = PacketHandler)
