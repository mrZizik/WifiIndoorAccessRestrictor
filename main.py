#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scapy.all import *
import os
import time
import thread
import ur
import sched, time

blacklist = []

def timerFunc(sc): 
    print "Updating white list"
    blacklist = urllib.urlopen("http://dagmeet.appspot.com/LIST")
    s.enter(60, 1, timerFunc, (sc,))



logfile = open("logs.txt","a+")
breaks=[]


def request(str):
	data = {}
	data["message"] = str
	url_values = urllib.urlencode(data)
	url = "http://dagmeet.appspot.com/NOTIFY"
	urllib.urlopen(url + "?" + url_values)

def getList()


def notify(addr):
    if addr not in breaks:
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        logfile.write("[{0}] - {1} from blacklist is in secured area\n".format(time, addr))
        print "[{0}] - {1} from blacklist is in secured area".format(time, addr)
        request("[{0}] - {1} from blacklist is in secured area".format(time, addr))
        breaks.append(addr)

def PacketHandler(pkt):
    if pkt.addr2 in blacklist:
        notify(pkt.addr2)
    elif pkt.addr1 in blacklist:
        notify(pkt.addr1)


s = sched.scheduler(time.time, time.sleep)
s.enter(60, 1, do_something, (s,))
s.run()

sniff(iface="mon0", prn = PacketHandler)



