
from bs4 import BeautifulSoup
from bs4.element import Comment
import requests
import urllib.request
import unicodedata

measurements = ["tablespoons", "teaspoons", "pounds", "cups", "cans", "packages", "jars", "ounces", "containers", "bushels", "tons", \
    "tablespoon", "teaspoon", "pound", "cup", "can", "package", "jar", "ounce", "container", "bushel", "ton"]

def parse(url):
    # parse website url
    webpage = requests.get(url, timeout=5)
    doc = BeautifulSoup(webpage.text, "html.parser")

    # get ingredients
    ingredients = []
    ingredientParse = doc.find_all("span", {"class": 'ingredients-item-name'})
    print("printing ingredients")
    for element in ingredientParse: 
        ingredients.append(element.text)
    quantities = []
    for ingredient in ingredients:

        quantity = []
        ingredient_name = ""

        # find alternate quantities
        alternateQuantity = ""
        if not (ingredient[0].isalpha() or ingredient[0] == " "):
            quantity = [unicodedata.numeric(ingredient[0])]
            if "(" in ingredient:
                alternateQuantity = ingredient.split('(')[1].split(')')[0]
            if alternateQuantity != "":
                quantity.append(alternateQuantity)
    
        if "," in ingredient:
            separated = ingredient.split(",")
            additional_directions = separated[1]

        for measurement in measurements:
            if measurement in ingredient:
                quantity[0] = str(quantity[0]) + " " + measurement
                ingredient_name = ingredient.split(measurement)[1].strip()
                print(quantity[0])
                print(ingredient_name)
                break
        
        quantities.append(quantity)

    print(quantities)

    # get directions
    directions = []
    instructions = doc.find_all("div", {"class": 'paragraph'})
    for i in instructions:
        # print(i.p.text)
        directions.append(i.p.text)

    return ingredients, quantities, directions