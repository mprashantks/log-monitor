import socketio
import time

sio = socketio.Client()


resource = 'resource1'
file = 'example.log'


@sio.event
def connect():
    print('Connected to Server !!')
    sio.emit('resource connection', resource)


@sio.event
def disconnect():
    print('Disconnected from Server !!')
    sio.emit('resource disconnection')


@sio.event
def read_log(_):
    print('Reading Logs')
    with open('example.log', 'rb') as read_obj:
        n = 10
        read_obj.seek(0, 2)
        pointer_location = read_obj.tell()
        while pointer_location >= 0 and n > 0:
            read_obj.seek(pointer_location)
            new_byte = read_obj.read(1)
            if new_byte == b'\n' or pointer_location == 0:
                n -= 1
            if n == 0:
                break
            pointer_location -= 1

    pointer_location += 1
    while True:
        with open('example.log', 'r') as read_obj:
            read_obj.seek(pointer_location)
            new_line = read_obj.readline()
            pointer_location = read_obj.tell()
            if not new_line:
                time.sleep(1)
                continue
            else:
                sio.emit('publish log', {'resource': resource, 'key': pointer_location, 'msg': new_line.rstrip('\n')})


sio.connect('http://127.0.0.1:8100')
sio.wait()
