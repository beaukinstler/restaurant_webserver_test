from flask import Flask, url_for, render_template, request, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import BASE, Restaurant, MenuItem
from db_command import *
import pdb

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
BASE.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def index():
    restaurants = get_all_restaurants()

    return render_template('index.html',restaurants=restaurants)
        

@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(res_id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.res_id)
    # return output
    user = 'admin'
    return render_template('menu.html',restaurant=restaurant,items=items,user=user)

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

@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    # output = ""
    # restaurant = session.query(Restaurant).filter_by(res_id=restaurant_id).one()
    # items = session.query(MenuItem).filter_by(restaurant_id=restaurant.res_id)

    # return "page to create a new menu item. Task 1 complete!"
    if request.method == 'POST':
        new_id = add_menu_item(restaurant_id,request.form['name'],request.form['price'])
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html',restaurant_id=restaurant_id)

# Task 2: Create route for editMenuItem function here

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    # return "page to edit a menu item. Task 2 complete!"
    if request.method == 'POST':
        update_menu_item(menu_id,request.form['name'],request.form['price'])
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        item = get_menu_item(menu_id)
        return render_template('editmenuitem.html',item=item)

# Task 3: Create a route for deleteMenuItem function here


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    
    if request.method == 'POST':
        if request.form['delete'] == 'Delete':
            delete_menu_item(menu_id)
        elif request.form['delete'] == 'Cancel':
            pass
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        item = get_menu_item(menu_id)
        return render_template('deletemenuitem.html',item=item)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
