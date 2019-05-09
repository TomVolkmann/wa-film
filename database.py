from sqlalchemy import Column, String, Integer, create_engine, Table, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
ENGINE = create_engine('sqlite:///app_db.db')

class Movies(Base):
    __tablename__ = "movies"

    id = Column('id', Integer, primary_key=True)
    title = Column('title', String, unique=True)
    release_date = Column('releaseDate', String)
    
    #referring  to the secondary table
    contacts = relationship("Contacts",secondary='link')

class Contacts(Base):
    __tablename__ = "contacts"

    id = Column('id', Integer, primary_key = True)
    name = Column('name', String)

    #referring  to the secondary table
    movies = relationship("Movies",secondary='link')

class Link(Base):
    __tablename__ = 'link'
    movies_id = Column(
    Integer, 
    ForeignKey('movies.id'), 
    primary_key = True)

    contact_id = Column(
   Integer, 
   ForeignKey('contacts.id'), 
   primary_key = True)


#    contact_movies= Table('contact_movies',
#     Base.metadata,
#     Column('contact_id',Integer ,ForeignKey ('contacts.id')),
#     Column('movie_id',Integer,ForeignKey('movies.id'))
# )

Base.metadata.create_all(bind=ENGINE)
Session = sessionmaker(bind=ENGINE)
session = Session() 

def saveNewMovie(input):   
    movie = Movies(title=input["title"],release_date=input["release_date"])
    contact = Contacts(name=input['contact'])

    movie.contacts.append(contact)

    #print(movie["title"])

    session.add(movie)
    session.add(contact)
    session.commit()
    session.close()




def get_movies():
    movie_totals = []
    for x in session.query(Movies, Contacts).filter(Link.movies_id == Movies.id, 
        Link.contact_id == Contacts.id).order_by(Link.movies_id).all():

        movie_total = {
            "id" : x.Movies.id,
            "title" : x.Movies.title,
            "release_date" : x.Movies.release_date,
            "name" : x.Contacts.name
        }
        movie_totals.append(movie_total)
    session.close()
    return movie_totals

def get_movie(movie_id):
    record = session.query(Movies).filter(Movies.id == movie_id).first()
    session.close()
    return record

def deleteMovies(id):
    session.delete(get_movie(id))
    session.commit()
    session.close()
