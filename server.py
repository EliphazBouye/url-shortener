from flask import Flask,redirect, request, render_template
from dotenv import load_dotenv, dotenv_values
from flask_sqlalchemy import SQLAlchemy
import string
import random

app = Flask(__name__)

load_dotenv()
config = dotenv_values(".env")

db = SQLAlchemy()

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{config['DB_USER']}:{config['DB_PASS']}@localhost/{config['DB_NAME']}"
db.init_app(app)

# MODEL
class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(250), unique=True, nullable=False)
    alias = db.Column(db.String(250))


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/create', methods=['POST'])
def create():
    if request.method == 'POST':
        url = request.form['url']
        KEY_LEN = 5
        def base_str():
            return (string.ascii_letters+string.digits)

        def key_gen():
            keylist = [random.choice(base_str()) for i in range(KEY_LEN)]
            return "".join(keylist)

        short = Url(url=url, alias=key_gen())
        db.create_all()
        db.session.add(short)
        db.session.commit()

    return redirect('all_short')

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