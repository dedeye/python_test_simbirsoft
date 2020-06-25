from flask import Flask, send_file, abort, render_template, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from PIL import Image, ImageFilter
from io import BytesIO
from pathlib import Path
import requests
import datetime
import uuid



def create_app():
    #create path to store images
    Path("img").mkdir(parents=True, exist_ok=True)

    return Flask(__name__)
    
app = create_app()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_type = db.Column(db.String(20), unique=False, nullable=False)
    processed_image = db.Column(db.String(80), unique=True, nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    # created = 
    # email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Animal %r>' % self.animal_type

    def serialize(self):
        return {
            'animal_type': self.animal_type, 
            'processed_image': self.processed_image,
            'created': self.created,
        }

uuid_generate = lambda: uuid.uuid4()



def get_url(animal):
    urls = {
        'cat': lambda: requests.get("http://aws.random.cat/meow").json()['file'],
        'dog': lambda: requests.get("http://shibe.online/api/shibes?count=1").json()[0],
        'fox': lambda: requests.get("https://randomfox.ca/floof/").json()['image'],
    }
    if animal in urls :
        return urls[animal]()
    else:
        return ""
    
def get_image(url):
    r = requests.get(url)
    image = Image.open(BytesIO(r.content)).convert('RGB')
    (w,h) = (1024, round(image.height * (1024/image.width)))
    image = image.resize((w,h))
    return image

def filter_image(image):
    # image = image.filter(ImageFilter.CONTOUR)
    image = image.filter(ImageFilter.SMOOTH_MORE)
    return image


@app.route('/animal/<animal_type>')
def getAnimal(animal_type):
    url = get_url(animal_type)
    if url == "":
        abort(404)
    
    image = get_image(url)
    image = filter_image(image)

    filename = "img/" + str(uuid_generate()) + ".png"

    image.save(filename)

    evt = Event(animal_type=animal_type, processed_image = filename)

    db.session.add(evt)
    db.session.commit()
    
    return send_file(filename, mimetype='image/png')


# @app.route('/history', defaults={'page': 1})
@app.route('/history')
def history():
    page = request.args.get('page', default = 1, type = int)
    output = request.args.get('output', default = 'html', type = str)

    events = Event.query.order_by(Event.created.desc()).paginate(page,10,error_out=False)


    if(output == 'html'):
        return render_template('template.html',events=events)
    elif(output == 'json'):
        return jsonify(events=[e.serialize() for e in events.items], 
                prev = url_for('history', page=events.prev_num, output = output) if events.has_prev else None,
                next =  'next' if events.has_next else None)
    else:
        abort(400)

@app.route('/history/static/<uuid>')
def history_(uuid):
    filename = "img/" + uuid + ".png"
    try:
        return send_file(filename)
    except (FileNotFoundError):
        abort(404)
    except:
        abort(502)

    