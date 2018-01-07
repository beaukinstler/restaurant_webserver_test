"""
build html snipits from db objects
"""


def restaurant_list(restaurants):
    output = "<div><ul>"
    for restaurant in restaurants:
        output += "<li>" + restaurant.name + "</li>"
    output += "</ul></div>"
    return output