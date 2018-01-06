"""
This file stores the comman db functions
to access the database with the app.
"""
from sqlalchemy import exc
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
    """
    Take and object, and update it in the database
    """
    try:
        ses.add(object_name)
        ses.commit()
    except exc.DatabaseError as e:
        print("Problem commiting the update in %s" % object_name.name)
        print("Error message:" % e.message)

# Get all the restaurants


# Find restaurant by ID
def get_restaurant(id_to_find):
    """ Using and id number, return Restaurant object """

    restaurant = ses.query(Restaurant).filter_by(res_id=id_to_find).one()
    return restaurant


# Add a new restaurant
def add_restaurant(restaurant_name):
    """

    """

    restaurant = Restaurant(name=restaurant_name)
    ses.add(restaurant)
    ses.commit()
    new_restaurant = \
        ses.query(Restaurant).filter_by(name=restaurant_name).one()
    return new_restaurant.res_id


# Delete a restaurant
def delete_restaurant(restaurant_id):
    """

    """
    restaurant = get_restaurant(restaurant_id)
    ses.delete(restaurant)
    ses.commit()


# Change a restaurant
def update_restaurant(res_id, name):
    """using an id, update the details of a restaurant

    Args:
    res_id - (int) id from the restaurant table, for the
             restaurant being changed.
    name - (string) New Name of the restaurant.
    """
    restaurant = get_restaurant(res_id)
    restaurant.name = name
    update_item(restaurant)


def get_menu_item(id_to_find):
    """ Using an ID, return a menu item

    Args:
    res_id - (int) id from the restaurant table, for the
             restaurant being changed.
    name - (string) New Name of the restaurant.

    Returns:
    (Object.MenuItem) Menu item object
    """

    item = ses.query(MenuItem).filter_by(men_id=id_to_find).one()
    return item


def add_menu_item(res_id, name, price=0):
    """
    Using an id and a restaurant, add a menu item

    Args:
    res_id - (int) id from the restaurant table, for the menu
             being added to.
    name - (string) name of the item
    price - (string) price of the item, no leading '$'

    Returns:
    id - (int) Id of the new item
    """

    item = MenuItem(name=name, price=price, restaurant_id=res_id)
    ses.add(item)
    ses.commit()
    new_item = \
        ses.query(MenuItem).filter_by(name=name, restaurant_id=res_id).one()
    return new_item.men_id


def delete_menu_item(men_id):
    # Delete a menu item using an id
    item = get_menu_item(men_id)

    ses.delete(item)
    ses.commit()


def update_menu_item(men_id, name, price):
    """using an id, update the details of a menu item"""

    item = get_menu_item(men_id)
    if str(name) != "":
        item.name = str(name)
    if str(price) != "":
        item.price = price

    update_item(item)
