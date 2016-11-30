#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scapy.all import *
blacklists = open("black.txt","r").read().split("\n")

def PacketHandler(pkt):
    if pkt.haslayer(Dot11):
        if pkt.addr2 in blacklists:
            print "Notify breach - {0}".format(pkt.addr2)


sniff(iface="mon0", prn = PacketHandler)
