from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
import random

db = SQLAlchemy()


class User(db.Model):
    query: db.Query
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    update_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    bookmark = db.relationship('Bookmark', backref='user')

    def __repr__(self):
        return f"<User: {self.username}>"


class Bookmark(db.Model):       #  e shkruajme ne njejes duke ndjekur naming conventions. Pra nje entitet i vetem
    query: db.Query
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=True)
    url = db.Column(db.Text, nullable=False)
    short_url = db.Column(db.String(3), nullable=False)
    visits = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    update_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def generate_short_characters(self):
        # do gjenerojme ne menyre rastesore karakteret per te krijuar url te shkurter
        characters = string.digits + string.ascii_letters   #  ketu kemi 123...9abcd....z
        picked_chars = "".join(random.choices(characters, k=3))   #  nga karakteret me lart marrim ne menyre rastesore 3 karaktere

        link = self.query.filter_by(short_url=picked_chars).first()  # pra do filtrojme te databaza nqs ky short_url ekziston

        if link:            # nqs do ekzistoje do gjenerojme tjeter
            self.generate_short_characters()
        else:              # ne te kundert kthen karakteret e perzgjedhura rastesisht
            return picked_chars

    def __init__(self, **kwargs):          # kur objekti krijohet therritet konstruktori. Pra i asenjojme short url kur krijohet objekti bookmark
        super().__init__(**kwargs)
        self.short_url = self.generate_short_characters()

    def __repr__(self):
        return f"<Bookmark: {self.id}. {self.body} -- created at {self.created_at}>"

