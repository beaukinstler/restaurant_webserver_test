from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import BASE, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
BASE.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(res_id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.res_id)
    output = ''
    for i in items:
        output += i.name
        output += '</br>'
        output += i.price
        output += '</br>'
        output += i.description
        output += '</br>'
        output += '</br>'
    return output

# Task 1: Create route for newMenuItem function here
def build_new_menuItem_form(res_id):
    """
    Build a form for adding a new restaurant to the database

    Args: String - Name of the restaurant TODO: format this like other function code headings
    """

    form = ''
    form += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>
                <h2>What's the details of the item?</h2>
                Name: <input name="name" type="text" label="Name" >
                Price: <input name="price" type="text" label="Price">
                <input type="submit" value="Submit"> </form>'''

    return form

@app.route('/restaurant/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id):
    output = ""
    restaurant = session.query(Restaurant).filter_by(res_id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.res_id)

    return "page to create a new menu item. Task 1 complete!"

# Task 2: Create route for editMenuItem function here

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
    return "page to edit a menu item. Task 2 complete!"

# Task 3: Create a route for deleteMenuItem function here


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
