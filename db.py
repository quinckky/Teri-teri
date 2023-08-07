'''
Module for database sqlalchemy classes
For bot.py file
'''

import os

from dotenv import load_dotenv
from sqlalchemy import Column, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    img_url = Column(Text)
    name = Column(String(64))
    dmg_type = Column(String(64))
    stars_count = Column(Integer)

    parameters = relationship('Parameter', back_populates='item', cascade='all, delete-orphan')

    skills = relationship('Skill', back_populates='item', cascade='all, delete-orphan')

class Parameter(Base):
    __tablename__ = 'parameters'
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'))
    name = Column(String(64))
    value = Column(String(64))

    item = relationship('Item', back_populates='parameters')

class Skill(Base):
    __tablename__ = 'skills'
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'))
    name = Column(String(64))
    dmg_type = Column(String(64))
    description = Column(Text)

    item = relationship('Item', back_populates='skills')
    
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)