from sqlalchemy import Column, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'
    
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer)
    title = Column(String(64))
    icon_url = Column(Text)
    dmg_type = Column(String(64))
    rarity = Column(Integer)

    properties = relationship('Property', back_populates='item', cascade='all, delete-orphan')

    skills = relationship('Skill', back_populates='item', cascade='all, delete-orphan')
    
    
class Property(Base):
    __tablename__ = 'properties'
    
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items.item_id'))
    name = Column(String(64))
    value = Column(String(64))

    item = relationship('Item', back_populates='properties')


class Skill(Base):
    __tablename__ = 'skills'
    
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items.item_id'))
    title = Column(String(64))
    description = Column(Text)
    dmg_type = Column(String(64))

    item = relationship('Item', back_populates='skills')
    
    
engine = create_engine('sqlite:///equipdex.db', echo=False)
Session = sessionmaker(bind=engine)
