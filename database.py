from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
ENGINE = create_engine('sqlite:///app_db.db')

class Movies(Base):
    __tablename__ = "movies"

    movie_id = Column('movie_id', Integer, primary_key=True)
    title = Column('title', String, unique=True)
    #release_data = Column('releaseDate', String)

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

