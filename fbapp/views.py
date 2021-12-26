# -*- coding: utf-8 -*-
#! python3

from flask_sock import Sock
from flask_apscheduler import APScheduler
from flask import Flask, render_template, url_for, request, copy_current_request_context, session

from time import strftime
import logging as lg

app = Flask(__name__)
app.config.from_object('config')
sockets = Sock(app)

scheduler = APScheduler()

scheduler.init_app(app)
scheduler.start()

from .utils import async_majBLE, find_content, scan

@scheduler.task("interval", id="scan_timer", seconds=900)
def job1():
    print("lancement timer scan")
    scan()
    print("timer scan exécuté")
    ## mode broadcast ne fonctionne pas...?
    # for client in clients:
    #     req = async_majBLE()
    #     if (clients[client]["ws"].connected):
    #         clients[client]["ws"].send(req)    

clients = {}
@sockets.route('/ws')
def echo_socket(_ws):
    global ws 
    ws = _ws
    peerName = ws.environ['werkzeug.socket'].getpeername()
    while ws.connected:
        if(peerName in clients):
            clients[peerName]["nbMessages"] += 1
        else:
            clients[peerName] = {}
            clients[peerName]["nbMessages"] = 0
            clients[peerName]["ws"] = ws

        message = ws.receive()
        print(message)
        req = async_majBLE()
        print(req)
        ws.send(req)

    clients.remove(peerName)
    print(ws.close_message + ws.close_reason)
    # print(type(ws))
    # print(ws.environ['werkzeug.socket'].getsockname() + ws.environ['werkzeug.socket'].getpeername())

@app.route('/')
@app.route('/index/')
def index():
    req1 = find_content("instant")
    req2 = find_content("all")

    return render_template('index.html', liste_data=req1, liste_all=req2)

if __name__ == "__main__":
    app.run()

class Client():
    def __init__(self) -> None:
        pass