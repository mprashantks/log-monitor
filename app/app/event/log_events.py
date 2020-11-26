from flask import request
from flask_socketio import emit, join_room, leave_room
from collections import deque

from .. import socketio


all_clients = []
last_n_logs = {}


@socketio.on('client connection')
def handle_client_connection(resource):
    print('Client Connected - [{}]'.format(request.sid))
    join_room(resource, request.sid)
    emit('display static log', list(last_n_logs.get(resource, [])))


@socketio.on('client disconnection')
def handle_client_disconnection(resource):
    leave_room(resource, request.sid)
    print('Client Disconnected - [{}]'.format(request.sid))


@socketio.on('resource connection')
def handle_resource_connection(resource):
    print('Resource [{}] Connected - [{}]'.format(resource, request.sid))
    emit('read_log')


@socketio.on('resource disconnection')
def handle_resource_disconnection(resource):
    print('Resource [{}] Disconnected - [{}]'.format(resource, request.sid))


@socketio.on('publish log')
def handle_new_log(data):
    print('Emitting !!', data['msg'])
    if data['resource'] not in last_n_logs:
        last_n_logs[data['resource']] = deque([], maxlen=10)
    last_n_logs[data['resource']].append(data)
    emit('display log', {'key': data['key'], 'msg': data['msg']}, room=data['resource'])
