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
    title = db.Column(db.String)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

    def addPost(input):
        post = Post(
            user_id = input["user_id"],
            title=input["title"],
            body=input["body"]
        )
        
        db.session.add(post)
        db.session.commit()
        db.session.close()

    def getPost(post_id):
        post = db.session.query(Post).filter(Post.id == post_id).first()
        db.session.close()
        return post

    def getPosts():
        total_posts = db.session.query(Post).join(User).all()
        for row in total_posts:
            for user in row.user:
                print(user.username)
        
        return total_posts

    def deletePost(id):
        db.session.delete(Post.getPost(id))
        db.session.commit()
        db.session.close()
    
class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)

    title_DE = db.Column(db.String, unique=True)
    title_EN = db.Column(db.String, unique=True)
    isReleased = db.Column(db.Integer)
    release_date = db.Column(db.String(140))
    format = db.Column(db.String)
    isColored = db.Column(db.Integer)
    language = db.Column(db.String)
    duration = db.Column(db.String)

    synopsis = db.Column(db.String)
    awards = db.Column(db.String)
    screenings = db.Column(db.String)
    supporters = db.Column(db.String)

    directors = db.Column(db.String)
    producers = db.Column(db.String)
    executive_producers = db.Column(db.String)
    editors = db.Column(db.String)
    cinematography = db.Column(db.String)
    sound_recordist = db.Column(db.String)
    sound_mix = db.Column(db.String)
    color = db.Column(db.String)
    img_url = db.Column(db.String)

    #referring  to the secondary table
    # contacts = db.relationship("Contact",secondary='link')

    def addMovie(input):   

        directors_str = create_String(input['directors'])

        movie = Movie(
            title_DE=input["title_DE"],
            title_EN=input["title_EN"],
            isReleased=input["isReleased"],
            release_date=input["release_date"],
            directors = directors_str
        )
        db.session.add(movie)
        db.session.commit()
        db.session.close()

    def getMovie(movie_id):
        record = db.session.query(Movie).filter(Movie.id == movie_id).first()
        db.session.close()
        return record

    def deleteMovie(id):
        db.session.delete(Movie.getMovie(id))
        db.session.commit()
        db.session.close()

class Contact(db.Model):
    __tablename__ = "contacts"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(32))

    def addContact(input):   
        contact = Contact(name=input["name"])
        
        db.session.add(contact)
        db.session.commit()
        db.session.close()

    def getContact(contact_id):
        record = db.session.query(Contact).filter(Contact.id == contact_id).first()
        db.session.close()
        return record
    
    def getContacts(contact_ids):
        name_list = []
        for contact_id in contact_ids:
            contact = db.session.query(Contact).filter(Contact.id == contact_id).first()
            name_list.append(contact.name)
        db.session.close()
        return name_list

    def deleteContact(id):
        movie_contacts = db.session.query(Movie_Contact).filter(Movie_Contact.contact_id == id).all()
        for mc in movie_contacts: 
            db.session.delete(mc)
            db.session.commit()

        db.session.delete(Contact.getContact(id))

        db.session.commit()
        db.session.close() 

class Movie_Contact(db.Model):
    __tablename__ = 'movie_contacts'

    id = db.Column('id', db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'))
    contact_type = db.Column(db.String)

    contact = db.relationship(Contact, backref="contacts")
    movie = db.relationship(Movie, backref="movies")

def create_String(contacts):
    contact_str = ""
    for contact in contacts:
        print(contact)
        if len(contact_str)>0:
            contact_str+=","
        contact_str+=str(contact)
    return contact_str
    