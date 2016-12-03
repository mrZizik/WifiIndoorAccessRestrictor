#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
from __future__ import unicode_literals 

import site 
import os.path 
import logging 
import json
site.addsitedir(os.path.join(os.path.dirname(__file__), 'libs')) 

import telegram 
from flask import Flask, request 


app = Flask(__name__) 

 
TOKEN = '#'
URL = 'dagmeet.appspot.com' 

global bot 
bot = telegram.Bot(token=TOKEN) 


@app.route('/HOOK', methods=['POST']) 
def webhook_handler(): 
    if request.method == "POST": 
        update = telegram.Update.de_json(request.get_json(force=True))
        try:
            chat_id = update.message.chat.id 
            text = update.message.text
            text = text.lower()
            bot.sendMessage(chat_id=chat_id, text='ТЕКСТ')
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



