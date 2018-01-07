"""
build html snipits from db objects
"""


def restaurant_list(restaurants):
    output = ""
    output += "<html><body>"
    output += "<h1> Restaurants: </h1>"
    output += "<div><ul>"
    for restaurant in restaurants:
        output += "<li>" + restaurant.name + "</li>"
    output += "</ul></div>"
    output += "</body></html>"
    return output