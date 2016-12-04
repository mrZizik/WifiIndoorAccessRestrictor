#!/usr/bin/env python
# -*- coding: utf-8 -*-


from time import gmtime, strftime
from scapy.all import *
import os
import time
import thread
import urllib3
http = urllib3.PoolManager()

from threading import Timer,Thread,Event

class perpetualTimer():

   def __init__(self,t,hFunction):
      self.t=t
      self.hFunction = hFunction
      self.thread = Timer(self.t,self.handle_function)
      self.thread.daemon = True

   def handle_function(self):
      self.hFunction()
      self.thread = Timer(self.t,self.handle_function)
      self.thread.start()

   def start(self):
      self.thread.start()

   def cancel(self):
      self.thread.cancel()







## blacklist = open("black.txt","r".read().split("\n")
logfile = open("logs.txt","a+")
breaks=[]
blacklist=[]


def getBlackList():
    return http.request("GET", "http://dagmeet.appspot.com/LIST").data.split("\n")

def updateBlackList():
    global blacklist
    print blacklist
    newbl = getBlackList()
    if blacklist != newbl:
        blacklist = newbl
        print "Blacklist updated: ",blacklist

def request(str):
    http.request("GET", "http://dagmeet.appspot.com/NOTIFY", fields={"mac": str})
    

def notify(addr):
    if addr not in breaks:
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        logfile.write("[{0}] - {1} is in secured area\n".format(time, addr))
        print "[{0}] - {1} is in secured area".format(time, addr)
        request("[{0}] - {1} is in secured area".format(time, addr))
        breaks.append(addr)

def PacketHandler(pkt):
    if pkt.addr2 in blacklist:
        notify(pkt.addr2)
    elif pkt.addr1 in blacklist:
        notify(pkt.addr1)

blacklist = getBlackList()
print "Blacklist ", blacklist

t = perpetualTimer(30,updateBlackList)
t.start()
sniff(iface="mon0", prn = PacketHandler)

