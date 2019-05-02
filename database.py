from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
ENGINE = create_engine('sqlite:///users.db')

class User(Base):
    __tablename__ = "user"

    user_id = Column('user_id', Integer, primary_key=True)
    username = Column('username', String, unique=True)

Base.metadata.create_all(bind=ENGINE)
Session = sessionmaker(bind=ENGINE)
session = Session() 