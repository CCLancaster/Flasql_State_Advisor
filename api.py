from models import app
from flask import jsonify, request
from crud.state_crud import get_all_states, get_state, create_state, update_state, destroy_state

@app.errorhandler(Exception)
def unhandled_exception(e):
    app.logger.error('Unhandled Exception: %s', (e))
    message_str = e.__str__()
    return jsonify(message=messsage_str.split(':')[0])

@app.route('/states', methods=['GET', 'POST'])
def state_index_create():
    if request.method == 'GET':
        return get_all_states()
    if request.method == 'POST':
        return create_state()
