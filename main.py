#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import gmtime, strftime
from scapy.all import *
blacklist = open("black.txt","r").read().split("\n")
logfile = open("logs.txt","a+")

def notify(addr):
    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    logfile.write("[{0}] - {1} from blacklist is in secured area".format(time, addr))
    print "[{0}] - {1} from blacklist is in secured area".format(time, addr)

def PacketHandler(pkt):
    if pkt.addr2 in blacklist:
        notify(pkt.addr2)
    elif pkt.addr1 in blacklist:
        notify(pkt.addr1)


sniff(iface="mon0", prn = PacketHandler)
