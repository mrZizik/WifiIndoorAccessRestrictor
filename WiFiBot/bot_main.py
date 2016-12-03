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


app = Flask(__name__) 

 
TOKEN = '313514427:AAHucA5unebq3-yPF8BzPpFBA_Z2khcsbz0'
URL = 'dagmeet.appspot.com' 
password = "6c37ff0650a9580bba66dc6334ef10f83ec3e19f9282bc29c6c6634718ab9aee" # Very strong password's hash
global bot 
bot = telegram.Bot(token=TOKEN) 
admins = []

def checkPassword(str):
    h = hashlib.sha256()
    h.update(str)
    return h.hexdigest() == password

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



