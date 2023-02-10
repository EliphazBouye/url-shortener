from flask import Flask, redirect, jsonify, request, url_for, render_template, flash
from dotenv import load_dotenv, dotenv_values
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import string
import random

config = dotenv_values(".env")
app = Flask(__name__)
app.secret_key = config['APP_KEY']
load_dotenv()

db = SQLAlchemy()

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{config['DB_USER']}:{config['DB_PASS']}@localhost/{config['DB_NAME']}"
db.init_app(app)

# MODEL
class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(250), unique=True, nullable=False)
    alias = db.Column(db.String(6), unique=True)
    clicks = db.Column(db.Integer, nullable=False)

    def to_json(self):
        return {
            "id": int(self.id),
            "url": str(self.url),
            "alias": str(self.alias),
        }


@app.post('/api/create')
def create():
    db.create_all()

    try:
        url = request.json['url']
        KEY_LEN = 5
        def base_str():
            return (string.ascii_letters+string.digits)

        def key_gen():
            keylist = [random.choice(base_str()) for i in range(KEY_LEN)]
            return "".join(keylist)

        short = Url(url=url, alias=key_gen())
        db.session.add(short)
        db.session.commit()
        return jsonify({"status": True, "message": "URL Added"})
    except IntegrityError:
        return jsonify({"status": False, "message": "URL Not Added"})


@app.route('/api/all_short')
def all_short():
    urls = Url.query.all()
    #db.session.query(Url).all()
    result = [url.to_json() for url in urls]
    return jsonify(result)
    

@app.route('/api/<alias>')
def alias(alias):
    res = db.session.query(Url).filter(Url.alias == alias)
    url = {}
    for row in res:
        url["url"] = row.url
    if url == {}:
        return jsonify({"flash": "Invalid URL"})
    return jsonify(url)

@app.route('/api/<int:id>/delete', methods = ['POST'])
def delete(id):
    if request.method == "POST":
        alias = db.get_or_404(Url, id)
        db.session.delete(alias)
        db.session.commit()
        return jsonify({"flash": "Alias Deleted"})
    return jsonify({"flash": 'Invalid alias'})
