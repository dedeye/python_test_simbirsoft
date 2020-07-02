from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
from pathlib import Path
import configparser
from animals.history import history
from animals.animal_cat import animal_cat
from animals.animal_dog import animal_dog
from animals.animal_fox import animal_fox

app = Flask(__name__)


# read config
config = configparser.ConfigParser()
config.read('config.txt')

app.config['SQLALCHEMY_DATABASE_URI'] = config['main'].get('db_file')
app.config['APP_REQUESTS_TIMEOUT'] = config['main'].getint('requests_timeout')
app.config['IMG_FOLDER'] = Path(config['main'].get('img_folder')).resolve()


# setup db
db = SQLAlchemy(app)


def setup_history_db(db):
    class Event(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        animal_type = db.Column(db.String(20), unique=False, nullable=False)
        processed_image = db.Column(db.String(80), unique=True, nullable=False)
        created = db.Column(db.DateTime, default=datetime.datetime.utcnow())

        def __repr__(self):
            return '<Animal %r>' % self.animal_type

        def serialize(self):
            return {
                'animal_type': self.animal_type,
                'processed_image': self.processed_image,
                'created': self.created,
            }

    class HistoryDBO(object):
        def store_event(self, animal_type, processed_image):
            evt = Event(animal_type=animal_type,
                        processed_image=processed_image)
            db.session.add(evt)
            db.session.commit()

        def get_events(self, page: int):
            events = Event.query.order_by(Event.created.desc())
            return events.paginate(page, 10, error_out=False)

    return HistoryDBO()


app.config["history.db"] = setup_history_db(db)


# import blueprints

app.register_blueprint(history)
app.register_blueprint(animal_cat)
app.register_blueprint(animal_dog)
app.register_blueprint(animal_fox)
