from flask import request, render_template, jsonify, send_file, \
    abort, url_for, Blueprint, current_app

# from animals.history_model import get_events
# from animals import db

history = Blueprint('history', __name__)


def create_json(events):

    events_serial = [e.serialize() for e in events.items]

    page = 'history.history_page'

    if(events.has_prev):
        prev = url_for(page, page=events.prev_num, output="json")
    else:
        prev = None

    if(events.has_next):
        next = url_for(page, page=events.next_num, output="json")
    else:
        next = None

    return jsonify(events=events_serial, prev=prev, next=next)


@history.record
def record(state):
    db = state.app.config.get("history.db")

    if db is None:
        raise Exception("This blueprint expects you to provide "
                        "database access through history.db")


@history.route('/history')
def history_page():

    page = request.args.get('page', default=1, type=int)

    output = request.args.get('output', default='html', type=str)

    db = current_app.config["history.db"]

    events = db.get_events(page)

    if(output == 'html'):
        return render_template('template.html', events=events)

    elif(output == 'json'):
        return create_json(events)

    else:
        abort(400)


@history.route('/history/static/<uuid>')
def history_by_uuid(uuid):
    filename = "img/" + uuid + ".png"

    return filename
    try:
        return send_file(filename)
    except (FileNotFoundError):
        abort(404)
