"""
This is a class to setup the data connections for a
restaurant menu web application
"""
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

BASE = declarative_base()

class Category(BASE):
    """
    Define restaurant class
    Extends a constant of an instance of declarative_base()
    """

    __tablename__ = 'category'

    category = Column(String(80), nullable=False)
    category_id =  Column(Integer, primary_key=True)

class Restaurant(BASE):
    """
    Define restaurant class
    Extends a constant of an instance of declarative_base()
    """

    __tablename__ = 'restaurant'

    name = Column(String(80), nullable=False)
    res_id = Column(Integer, primary_key=True)

    category_id =  Column(Integer, ForeignKey('category.category_id'))
    category = relationship(Category)

class MenuItem(BASE):
    """
    Define restaurant class
    Extends a constant of an instance of declarative_base()
    """

    __tablename__ = 'menu_item'

    name = Column(String(80), nullable=False)
    men_id = Column(Integer, primary_key=True)

    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))

    restaurant_id = Column(Integer, ForeignKey('restaurant.res_id'))

    restaurant = relationship(Restaurant)

    @property
    def serialize(self):
        #Returns object in easily serializeable format
        return {
            'name': self.name,
            'description': self.description,
            'id': self.men_id,
            'price': self.price,
            'course': self.course    
        }

ENGINE = create_engine('sqlite:///restaurantmenu.db')

BASE.metadata.create_all(ENGINE)
