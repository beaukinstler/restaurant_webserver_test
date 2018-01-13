"""
build html snipits from db objects
"""


def restaurant_list(restaurants):
    output = ""
    output += "<h1> Restaurants: </h1>"
    output += "<div><ul>"
    for restaurant in restaurants:
        output += "<li>" + restaurant.name + " - " + str(restaurant.res_id) + "</li>"
    output += "</ul></div>"
    return output