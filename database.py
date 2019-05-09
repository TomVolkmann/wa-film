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
    

m1 = Movies(id = 0,title="Test", release_date="19.02.2019")
m2 = Movies(id = 1,title="Test1", release_date="18.02.2019")

c1 = Contacts(id = 0, name="Hans")
c2 = Contacts(id = 1, name="Franz")

m1.contacts.append(c1)

session.add(m1)
session.add(m2)
session.add(c1)
session.add(c2)

session.commit()
session.close()