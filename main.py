#!/usr/bin/env python
# -*- coding: utf-8 -*-


from time import gmtime, strftime
from scapy.all import *
import os
import time
import thread
import urllib3
http = urllib3.PoolManager()

## blacklist = open("black.txt","r".read().split("\n")
logfile = open("logs.txt","a+")
breaks=[]
blacklist=[]
starttime=time.time()

while True:
    blacklist = http.request("GET", "http://dagmeet.appspot.com/LIST").data.split("\n")
    breaks = []
    print blacklist
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))

def getBlackList():
    http.request("GET", "http://dagmeet.appspot.com/LIST").data.split("\n")

def request(str):
    http.request("GET", "http://dagmeet.appspot.com/NOTIFY", fields={"mac": str})
    


def notify(addr):
    if addr not in breaks:
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        logfile.write("[{0}] - {1} not in whitelist is in secured area\n".format(time, addr))
        print "[{0}] - {1} from blacklist is in secured area".format(time, addr)
        request("[{0}] - {1} from blacklist is in secured area".format(time, addr))
        breaks.append(addr)

def PacketHandler(pkt):
    if pkt.addr2 in blacklist:
        notify(pkt.addr2)
    elif pkt.addr1 in blacklist:
        notify(pkt.addr1)


getBlackList()
sniff(iface="mon0", prn = PacketHandler)
