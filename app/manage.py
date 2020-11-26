import unittest

from flask_script import Manager

from app import create_app, socketio

app = create_app()
app.app_context().push()

manager = Manager(app)


@manager.command
def run():
    socketio.run(app, host='0.0.0.0', port=8100)


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
