from animals.common import get_uuid, get_filename_from_uuid
from flask import Blueprint, current_app, send_file, abort
from animals.image_processing import image_process
import requests


animal_cat = Blueprint('animal_cat', __name__)


def get_cat_raw_image():
    timeout = current_app.config["APP_REQUESTS_TIMEOUT"]

    # http://aws.random.cat/ went unavailable (at least from my network)
    # so I changed it to cataas.com
    return requests.get("https://cataas.com/cat", timeout=timeout).content


def save_event(uuid):
    db = current_app.config["history.db"]
    db.store_event("cat", uuid)


@animal_cat.route('/animal/cat')
def cat():
    try:
        raw_image = get_cat_raw_image()
        processed_image = image_process(raw_image)

    except Exception:
        abort(500)
    
    uuid = get_uuid()

    filename = get_filename_from_uuid(uuid)
    processed_image.save(filename)

    save_event(uuid)

    return send_file(filename, mimetype='image/png')
