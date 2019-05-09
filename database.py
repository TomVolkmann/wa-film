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

def saveNewMovie(input):   
    movie = Movies(title=input["title"],release_date=input["release_date"])
    contact = Contacts(name=input['contact'])

    movie.contacts.append(contact)

    #print(movie["title"])

    session.add(movie)
    session.add(contact)
    session.commit()
    session.close()

def getMovies():
    movies = session.query(Movies).all()
    print(type(movies))
    session.close()
    return movies

def get_movie(movie_id):
    record = session.query(Movies).filter(Movies.id == movie_id).first()
    session.close()
    return record

def deleteMovies(id):

    session.delete(get_movie(id))
    session.commit()
    session.close()
    

# m1 = Movies(title="Test", release_date="19.02.2019")
# m2 = Movies(title="Test1", release_date="18.02.2019")

# c1 = Contacts(name="Hans")
# c2 = Contacts(name="Franz")

# m1.contacts.append(c1)

# session.add(m1)
# session.add(m2)
# session.add(c1)
# session.add(c2)

# session.commit()
# session.close()