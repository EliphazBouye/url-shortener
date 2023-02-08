from flask import Flask,redirect, request, render_template
from .db import db
from .Model import Url
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/create', methods=['POST'])
def create():
    if request.method == 'POST':
        url = request.form['url']
        short = Url(url=url, alias='ttttt')
        db.create_all()
        db.session.add(short)

    return render_template("result.html",result = Short.query.all())

# @app.route('/<alias>')
# def short(alias):
#     return redirect("https://github.com/eliphazbouye")
