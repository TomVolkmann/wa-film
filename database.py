from sqlalchemy import Column, String, Integer, create_engine, Table, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
ENGINE = create_engine('sqlite:///app_db.db')

contact_movies= Table('contact_movies',
    Base.metadata,
    Column('contact_id',Integer ,ForeignKey ('contacts.id')),
    Column('movie_id',Integer,ForeignKey('movies.id'))
)

class Movies(Base):
    __tablename__ = "movies"

    id = Column('id', Integer, primary_key=True)
    title = Column('title', String, unique=True)
    release_date = Column('releaseDate', String)
    
    #referring  to the secondary table
    contacts = relationship("Contacts",secondary=contact_movies)

class Contacts(Base):
    __tablename__ = "contacts"

    id = Column('id', Integer, primary_key = True)
    name = Column('name', String)

    #referring  to the secondary table
    movies = relationship("Movies",secondary=contact_movies)


Base.metadata.create_all(bind=ENGINE)
Session = sessionmaker(bind=ENGINE)
session = Session() 

def saveNewMovie(movie_id,title):
    movie = Movies(movie_id=movie_id, title=title)

    session.add(movie)
    session.commit()
    session.close()

def getMovies():
    movies = session.query(Movies).all()
    print(type(movies))
    session.close()
    return movies
    
getMovies()

