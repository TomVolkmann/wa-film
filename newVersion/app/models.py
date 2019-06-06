#pylint: skip-file
from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, String, Integer, create_engine, Table, ForeignKey

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Movies(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), unique=True)
    release_date = db.Column(db.String(140))
    
    #referring  to the secondary table
    contacts = db.relationship("Contacts",secondary='link')

    def saveNewMovie(input):   
        movie = Movies(title=input["title"],release_date=input["release_date"])
        contact = Contacts(name=input['contact'])

        movie.contacts.append(contact)

        db.session.add(movie)
        db.session.add(contact)
        db.session.commit()
        db.session.close()

    def get_movies():
        movies = []
        for x in db.session.query(Movies, Contacts).filter(Link.movies_id == Movies.id, 
            Link.contact_id == Contacts.id).order_by(Link.movies_id).all():

            movie_total = {
                "id" : x.Movies.id,
                "title" : x.Movies.title,
                "release_date" : x.Movies.release_date,
                "name" : x.Contacts.name
            }
            movies.append(movie_total)
        db.session.close()
        return movies

    def get_movie(movie_id):
        record = db.session.query(Movies).filter(Movies.id == movie_id).first()
        db.session.close()
        return record

    def deleteMovies(id):
        db.session.delete(Movies.get_movie(id))
        db.session.commit()
        db.session.close()

class Contacts(db.Model):
    __tablename__ = "contacts"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(32))

    #referring  to the secondary table
    movies = relationship("Movies",secondary='link')

class Link(db.Model):
    movies_id = db.Column(db.Integer, ForeignKey('movies.id'), primary_key = True)
    contact_id = db.Column(db.Integer, ForeignKey('contacts.id'), primary_key = True)
