from flask import Flask,redirect, request, url_for, render_template, flash
from dotenv import load_dotenv, dotenv_values
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from jinja2 import Environment
from jinja2.loaders import FileSystemLoader
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
    alias = db.Column(db.String(250), unique=True)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/create', methods=['POST'])
def create():
    db.create_all()

    try:
        if request.method == 'POST':
            url = request.form['url']
            KEY_LEN = 5
            def base_str():
                return (string.ascii_letters+string.digits)

            def key_gen():
                keylist = [random.choice(base_str()) for i in range(KEY_LEN)]
                return "".join(keylist)

            short = Url(url=url, alias=key_gen())
            db.session.add(short)
            db.session.commit()
            return redirect(url_for('all_short'))
    except IntegrityError:
        flash("Url already use")
        return redirect(url_for('index'))


@app.route('/all_short')
def all_short():
    return render_template("result.html", result = Url.query.all(), base = request.url_root)

@app.route('/<alias>')
def alias(alias):
    res = db.session.query(Url).filter(Url.alias == alias)
    url = []
    for row in res:
        url.append(row.url)
    return redirect(url[0])

@app.route('/<int:id>/delete', methods = ['POST'])
def delete(id):
    if request.method == "POST":
        alias = db.get_or_404(Url, id)
        db.session.delete(alias)
        db.session.commit()
        flash("Alias Deleted")
        return redirect(url_for('all_short'))
    flash("Invalid alias")
    return redirect(url_for('all_short'))