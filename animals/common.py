import uuid
from flask import current_app


def get_uuid():
    return str(uuid.uuid4())


def get_filename_from_uuid(uuid):
    return str(current_app.config["IMG_FOLDER"]) + "/" + uuid + ".png"
