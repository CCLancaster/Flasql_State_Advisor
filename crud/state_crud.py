from flask import jsonify, redirect
from models import db, User

# Index
def get_all_states():
    all_states = State.query.all()
    if len(all_states) > 0:
        results = [state.as_dict() for state in all_states]
    else:
        results = []
    return jsonify(results)

# Show
def get_state():
    state = State.query.get(id)
    if state: 
        return jsonify(state.as_dict())
    else:
        raise Exception('No State at this id {}'.format(id))

# Create
def create_state(name, capital, date_est, abbr, motto):
    new_state = State(name=name, capital=capital or None, date_est=date_est or None, abbr=abbr or None, motto=motto or None)
    db.session.add(new_state)
    db.session.commit()
    return jsonify(new_state.as_dict())

# Update
def update_state(id, name, capital, date_est, abbr, motto):
    state = State.query.get(id)
    if state:
        state.name = name or state.name
        state.capital = capital or state.capital
        state.date_est = date_est or state.date_est
        state.abbr = abbr or state.abbr
        state.motto = motto or state.motto
        db.session.commit()
        return jsonify(state.as_dict())
    else: 
        raise Exception('No State at this id {}'.format(id))

# Destroy
def destroy_state(id):
    state = State.query.get(id)
    if state:
        db.session.delete(state)
        db.session.commit()
        return redirect('/states')
    else:
        raise Exception('No State at id {}'.format(id))