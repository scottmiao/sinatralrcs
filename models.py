from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///.\\tmp\\test.db'
db = SQLAlchemy(app)


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    lyrics = db.Column(db.Text)
    length = db.Column(db.Integer)
    released_on = db.Column(db.DateTime)

    def __init__(self, title, lyrics, length, released_on):
        self.title = title
        self.lyrics = lyrics
        self.length = length
        self.released_on = released_on

    def __repr__(self):
        return '<Song [%r] [%r] [%r] [%r]>' % (self.title,
                                               self.lyrics,
                                               self.length,
                                               self.released_on)


def init_db():
    db.create_all()
