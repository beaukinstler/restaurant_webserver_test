"""
build html snipits from db objects
"""


def restaurant_list(restaurants):
    output = ""
    output += "<h1> Restaurants: </h1>"
    output += "<div><ul>"
    for restaurant in restaurants:
        output += "<li>" + restaurant.name + " - " + str(restaurant.res_id)
        output += "- <a href='/restaurant/" + str(restaurant.res_id) + "/edit'>Edit</a> - "
        output += "<a href='/restaurant/" + str(restaurant.res_id) + "/delete'>Delete</a>"
        output += "</li>"
    output += "</ul></div>"
    return output

def nav_links():
    """
    Purpose: Links to have on top and bottom of each page
    """
    output = ""
    paths = {'home': '/restaurants',
             'add new restaurant': '/restaurants/new',
             'about': '#'}
    
    last_key = paths.keys()[-1]
    for label,link in paths.items():
        output += "<a href='"
        output += str(link)
        output += "'>"
        output += str(label)
        output += "</a>"
        if label != last_key:
            output += " - "
    
    return output

