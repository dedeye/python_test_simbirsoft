from animals.common import get_uuid, get_filename_from_uuid
from flask import Blueprint, current_app, send_file, abort
from animals.image_processing import image_process
import requests


animal_fox = Blueprint('animal_fox', __name__)


def get_fox_raw_image():
    timeout = current_app.config["APP_REQUESTS_TIMEOUT"]

    fox_url = "https://randomfox.ca/floof/"
    image_url = requests.get(fox_url, timeout=timeout).json()['image']
    return requests.get(image_url, timeout=timeout).content


def save_event(uuid):
    try:
        db = current_app.config["history.db"]
        db.store_event("fox", uuid)
    except Exception as e:
        current_app.logger.error('can not save event: {}'.format(e))


@animal_fox.route('/animal/fox')
def fox():
    try:
        raw_image = get_fox_raw_image()
        processed_image = image_process(raw_image)

    except Exception as e:
        current_app.logger.error('can not serve /animal/fox: {}'.format(e))
        abort(500)

    uuid = get_uuid()

    filename = get_filename_from_uuid(uuid)
    processed_image.save(filename)

    save_event(uuid)

    return send_file(filename, mimetype='image/png')
