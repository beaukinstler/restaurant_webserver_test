"""
This file stores the comman db functions
to access the database with the app.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, BASE, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
BASE.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
ses = DBSession()

# db update function
def update_item(object_name):
    ses.add(object_name)
    ses.commit()

# Get all the restaurants

# Find restaurant by ID
def get_restaurant(id_to_find):
    """ Using and id number, return Restaurant object """

    current = ses.query(Restaurant).filter_by(res_id=id_to_find).one()
    return current

# Add a new restaurant

# Delete a restaurant

# Change a restaurant
def update_restaurant(res_id, name):
    """using an id, update the details of a restaurant"""

    restaurant = get_restaurant(res_id)
    restaurant.name = name
    update_item(restaurant)

# Add a menu item

# Delete a menu item

# Update a menu item