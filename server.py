from flask import Flask,redirect

app = Flask(__name__)
@app.route('/')
def index():
    return "Flask URL-shortener"

@app.post('/create')
def create():


@app.route('/<alias>')
def short(alias):
    return redirect("https://github.com/eliphazbouye")
