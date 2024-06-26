# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import DeclarativeBase
# from app import db

# engine = create_engine('sqlite:///database.db', echo=True)
# db_session = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=engine))
# Base = declarative_base()
# Base.query = db_session.query_property()

# # Set your classes here.

# print("is this running")

# '''
# class User(Base):
#     __tablename__ = 'Users'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(120), unique=True)
#     email = db.Column(db.String(120), unique=True)
#     password = db.Column(db.String(30))

#     def __init__(self, name=None, password=None):
#         self.name = name
#         self.password = password
# '''

# # Create tables.
# Base.metadata.create_all(bind=engine)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from app import db

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String)

with app.app_context():
    db.create_all()