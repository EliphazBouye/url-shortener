from .db import db

class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(250), unique=True)
    alias = db.Column(db.String(120), unique=True)

    def __init__(self, url, alias):
        self.url = url
        self.alias = alias

    def __repr__(self):
        return '<Url %r>' % Url.url

