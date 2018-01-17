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
@app.route('/menu')
def Index():
    '''
    Main landing page, shows all menu items on first restuarant
    '''
    restaurants = session.query(Restaurant)
    # items = session.query(MenuItem).filter_by(restaurant_id = restaurant.res_id)
    output = "<ul>"
    output = "<li> NAME - ID</li>"
    for res in restaurants:
        output += "<li><a href='/restaurant/{1}/menu'>{0} - {1}</a></li>".format(res.name,res.res_id)
    output += "</ul>"
    return output

@app.route('/restaurant/<int:res_id>/menu')
def Menu(res_id):
    '''
    Menu for a restaurant
    '''
    restaurant = session.query(Restaurant).filter_by(res_id=res_id).first()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.res_id)
    output = "<h1>Menu for {}</h1>".format(restaurant.name)
    output += "<ul>"
    for item in items:
        output += "<li>{}</li>".format(item.name,)
    output += "</ul>"
    return output

if __name__ == '__main__':
      app.debug = True
      app.run( host = '0.0.0.0', port = 5001 )


