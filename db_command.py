"""
This file stores the comman db functions
to access the database with the app.
"""
from sqlalchemy import exc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, BASE, MenuItem, Category

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

# Print out all the restaurants
def list_all_restaurants():
    """
    List all restaurants by name and id, order based on data table
    """
    
    restaurants = ses.query(Restaurant)

    for restaurant in restaurants:
        print("Name: {}, ID: {}".format(str(restaurant.name), str(restaurant.res_id)))


def get_all_restaurants():
    """
    Get all restaurants by name and id, order based on data table
    Returns: An iterable list of restaurant objects
    """
    
    return ses.query(Restaurant)


# Find restaurant by ID
def get_restaurant(id_to_find):
    """ Using and id number, return Restaurant object """

    restaurant = ses.query(Restaurant).filter_by(res_id=id_to_find).one()
    return restaurant


# Add a new restaurant
def add_restaurant(restaurant_name,category_id):
    """

    """

    restaurant = Restaurant(name=restaurant_name,category_id=category_id)
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

def get_all_menu_items(res_id):
    """ Using an ID, return a menu item

    Args:
    res_id - (int) id from the restaurant table, for which
             menu to return
    Returns:
    List of (Object.MenuItem) Menu item objects
    """

    items = ses.query(MenuItem).filter_by(restaurant_id=res_id)
    return items


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


def add_menu_item(res_id, name, description, price=0):
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

    item = MenuItem(name=name, price=price, \
        restaurant_id=res_id, description=description)
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


def update_menu_item(men_id, name, description, price):
    """using an id, update the details of a menu item"""

    item = get_menu_item(men_id)
    if str(name) != "":
        item.name = str(name)
    if str(description) != "":
        item.description = str(description)
    if str(price) != "":
        item.price = str(price)

    update_item(item)


# Return all the categories
def get_all_categories():
    """
    Get all restaurants by name and id, order based on data table
    Returns: An iterable list of restaurant objects
    """
    
    return ses.query(Category)

# Add a new restaurant
def add_category(category_name):
    """

    """

    category = Category(category=category_name)
    ses.add(category)
    ses.commit()
    new_category = \
        ses.query(Category).filter_by(category=category_name).one()
    return new_category.category_id

# get a category
def get_category(category_id):
    """
    Return a category object
    """

    category =  ses.query(Category).filter_by(category_id=category_id).one()
    return category


def update_category(category_id, category_name):
    """using an id, update the details of a restaurant

    Args:
    category_id - (int) id from the catgeory table, for the
             restaurant being changed.
    category_name - (string) New Name of the category.
    """
    category = get_category(category_id)
    category.category = category_name
    update_item(category)

def delete_category(category_id):
    """using an id, delete a category

    Args:
    category_id - (int) id from the catgeory table, for the
             restaurant being changed.
    category_name - (string) New Name of the category.
    """
    cat = get_category(category_id)

    ses.delete(cat)
    ses.commit()