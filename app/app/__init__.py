from flask import Flask
from flask_socketio import SocketIO


socketio = SocketIO(cors_allowed_origins="*")


def create_app():
    application = Flask(__name__)
    application.debug = False
    application.config['SECRET_KEY'] = 'secret!'

    attach_controller(application)

    attach_event()

    socketio.init_app(application)
    return application


def attach_controller(application):
    from .controller.log import log

    application.register_blueprint(log, url_prefix='/log')


def attach_event():
    from .event import log_events
