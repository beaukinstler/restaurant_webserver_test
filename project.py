from flask import Flask, url_for, render_template, request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import BASE, Restaurant, MenuItem, Category
from db_command import *
from restaurants_views import *
import pdb


app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
BASE.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants')
def index():
    restaurants = get_all_restaurants()

    return render_template('index.html',restaurants=restaurants)
        

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(res_id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.res_id)
    # return output
    user = 'admin'
    return render_template('menu.html',restaurant=restaurant,items=items,user=user)

@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        new_id = add_restaurant(request.form['name'],request.form['option'])
        flash("Restaurant added!")
        return redirect(url_for('restaurantMenu', restaurant_id=new_id))
    else:
        categories = get_all_categories()
        return render_template('newrestaurant.html',categories=categories)

@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant():
    if request.method == 'POST':
        new_id = update_restaurant(restaurant_id,request.form['name'],request.form['category_id'])
        flash("Restaurant updated!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return "TODO: form for updating a restaurant"

@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    if request.method == 'POST':
        delete_restaurant(restaurant_id)
        flash("Restaurant deleted!")
        return redirect(url_for('index'))
    else:
        restaurant = get_restaurant(restaurant_id)
        return render_template('deleterestaurant.html',restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    # output = ""
    # restaurant = session.query(Restaurant).filter_by(res_id=restaurant_id).one()
    # items = session.query(MenuItem).filter_by(restaurant_id=restaurant.res_id)

    if request.method == 'POST':
        new_id = add_menu_item(restaurant_id,request.form['name'],request.form['description'],request.form['price'])
        flash("New menu item created!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html',restaurant_id=restaurant_id)

# Task 2: Create route for editMenuItem function here

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    # return "page to edit a menu item. Task 2 complete!"
    if request.method == 'POST':
        update_menu_item(menu_id, request.form['name'], request.form['description'], request.form['price'])
        flash("Item updated!")
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
            flash("Item deleted!")
        elif request.form['delete'] == 'Cancel':
            pass
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        item = get_menu_item(menu_id)
        return render_template('deletemenuitem.html',item=item)

@app.route('/restaurant/<int:restaurant_id>/json', methods=['GET'])
def getAllMenuItemJson(restaurant_id):
    restaurants = get_all_menu_items(restaurant_id)
    return jsonify(MenuItems=[res.serialize for res in restaurants])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/json', methods=['GET'])
def getMenuItemJson(restaurant_id, menu_id):
    item = get_menu_item(menu_id)
    return jsonify(MenuItems=item.serialize)

@app.route('/categories', methods=['GET'])
def getAllCategories():
    categories = get_all_categories()

    return render_template('categories.html',categories=categories)

@app.route('/category/<int:category_id>', methods=['GET'])
def category(category_id):
    category = get_category(category_id)

    return render_template('category.html',category=category)

@app.route('/category/new', methods=['GET', 'POST'])
def newCategory():
    if request.method == 'POST':
        new_id = add_category(request.form['category'])
        flash("Category added!")
        return redirect(url_for('getAllCategories'))
    else:
        return render_template('newcategory.html')

@app.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
def editCategory(category_id):
    if request.method == 'POST':
        update_category(category_id, request.form['category_name'])
        flash("Category updated!")
        return redirect(url_for('getAllCategories'))
    else:
        category = get_category(category_id)
        return render_template('editcategory.html',category=category)

@app.route('/category/<int:category_id>/delete', methods=['GET','POST'])
def deleteCategory(category_id):

    if request.method == 'POST':
        if request.form['delete'] == 'Delete':
            delete_category(category_id)
            flash("Category deleted!")
        elif request.form['delete'] == 'Cancel':
            pass
        return redirect(url_for('getAllCategories'))
    else:
        category = get_category(category_id)
        return render_template('deletecategory.html',category=category)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
