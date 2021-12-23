# -*- coding: utf-8 -*-

import asyncio
import websockets
from flask import Flask, render_template, url_for, request, copy_current_request_context, session


from time import strftime
import logging as lg

app = Flask(__name__)
app.config.from_object('config')

from .utils import async_majBLE, find_content, BaseThread

@app.route('/')
@app.route('/index/')
def index():
    req1 = find_content("instant")
    req2 = find_content("all")

    # if 'img' in request.args:
    #     img = request.args['img']
    #     og_url = url_for('index', img=img, _external=True)
    #     og_image = url_for('static', filename=img, _external=True)
    # else:
    #     og_url = url_for('index', _external=True)
    #     og_image = url_for('static', filename='tmp/sample.jpg', _external=True)

    # description = "Toi, tu sais comment utiliser la console ! "
    # page_title = "Le test ultime"

    # og_description = "Découvre qui tu es vraiment en faisant le test ultime !"
    return render_template('index.html', liste_data=req1, liste_all=req2)
                        #   user_name='Julio',
                        #   user_image=url_for('static', filename='img/profile.png'),
                        #   description=description,
                        #   blur=True,
                        #   page_title=page_title,
                        #   og_url=og_url,
                        #   og_image=og_image,
                        #   og_description=og_description)

@ws.on_raw_message
def raw_message_handler(message):
    print(message)

# @socketio.on('client_connected')
# def handle_client_connect_event(json):
#     print('received json: {0}'.format(str(json)))
#     req = async_majBLE()
#     emit('majData', req, broadcast=True)
#     print(req)


# @socketio.on('json_button', namespace=None)
# def handle_json_button(*args):
#     # it will forward the json to all clients.
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response', {'data': args[1], 'count': session['receive_count']})
#     send(args[1], json=True)

# @socketio.on('alert_button', namespace=None)
# def handle_alert_event(*args):
#     # it will forward the json to all clients.
#     print('Message from client was {0}'.format(args[1]))
#     emit('alert', 'Message from backend')

# @socketio.on('message')
# def handle_message(*args):
#     if(args[0] == "json_button"):
#         session['receive_count'] = session.get('receive_count', 0) + 1
#         emit('my_response', {'data': args[1], 'count': session['receive_count']})
#         send(args[1], json=True)
#     elif(args[0] == "alert_button"):
#         print('Message from client was {0}'.format(args[1]))
#         emit('alert', 'Message from backend')
      
# @socketio.on('disconnect_request')
# def disconnect_request():
#     @copy_current_request_context
#     def can_disconnect():
#         disconnect()

#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': 'Disconnected!', 'count': session['receive_count']},
#          callback=can_disconnect)

# def cb_retour(req):
#     send('maj_data', req, json=True, broadcast=True)

if __name__ == "__main__":
    app.run()