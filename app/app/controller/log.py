from flask import current_app
from flask import Blueprint, request

log = Blueprint('log', __name__)


@log.route('/test', methods=['GET'])
def test_endpoint():
    current_app.logger.info('Test API')
    data = request.args
    return {'hello': '3'}
