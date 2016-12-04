#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
from __future__ import unicode_literals 

import site 
import os.path 
import logging 
import json
import hashlib
site.addsitedir(os.path.join(os.path.dirname(__file__), 'libs')) 

import telegram 
from flask import Flask, request 

from google.appengine.ext import db




app = Flask(__name__) 

 
TOKEN = ''
URL = 'dagmeet.appspot.com' 
password = "" # Very strong password's hash
global bot 
bot = telegram.Bot(token=TOKEN) 
admins = []

def checkPassword(str):
    h = hashlib.sha256()
    h.update(str)
    return h.hexdigest() == password

class Record(db.Model):
    address = db.StringProperty()


@app.route('/LIST', methods=['GET']) 
def getList():
    records = db.GqlQuery("SELECT * FROM Record")
    response = ""
    for record in records:
        response+=record.address
        response+="\n"
    return response

def addRecord(str):
    str = str.replace("-","")
    str = str.replace("'","")
    record = Record(address=str)
    record.put()

def deleteRecord(str):
    str = str.replace("-","")
    str = str.replace("'","")
    records = db.GqlQuery("SELECT * FROM Record WHERE address=:1",str)
    for record in records:
        record.delete()




@app.route('/NOTIFY', methods=['GET']) 
def notify():
    for admin in admins:
        bot.sendMessage(chat_id=admin, text=request.args.get("mac"))

@app.route('/HOOK', methods=['POST']) 
def webhook_handler(): 
    if request.method == "POST": 
        update = telegram.Update.de_json(request.get_json(force=True))
        try:
            chat_id = update.message.chat.id 
            text = update.message.text
            text = text.lower()
            if text.startswith("/admin"):
                data = text.split(" ")
                if checkPassword(data[1]):
                    admins.append(chat_id)
                    bot.sendMessage(chat_id=chat_id, text="Access granted")
                else:
                    bot.sendMessage(chat_id=chat_id, text="Access denied")
            if text.startswith("/add") and chat_id in admins:
                data = text.split(" ")
                if len(data)==2:
                    addRecord(data[1])
                    bot.sendMessage(chat_id=chat_id, text="Added "+data[1])
                else:
                    bot.sendMessage(chat_id=chat_id, text="Syntax error; /add <mac_addr>")
            if text.startswith("/delete") and chat_id in admins:
                data = text.split(" ")
                if len(data)==2:
                    deleteRecord(data[1])
                    bot.sendMessage(chat_id=chat_id, text="Deleted "+data[1])
                else:
                    bot.sendMessage(chat_id=chat_id, text="Syntax error; /delete <mac_addr>")
            if text.startswith("/list") and chat_id in admins:
                bot.sendMessage(chat_id=chat_id, text=getList())
            logging.getLogger().setLevel(logging.INFO) 
            logging.info('===============TEXT=================' + text) 
        except AttributeError:
            print "a"
    return 'ok' 




#А вот так подключается вебхук 
@app.route('/set_webhook', methods=['GET', 'POST']) 
def set_webhook(): 
    s = bot.setWebhook('https://%s/HOOK' % URL) 
    if s: 
        return "webhook setup ok" 
    else: 
        return "webhook setup failed" 

@app.route('/') 
def index(): 
    return '.' 





