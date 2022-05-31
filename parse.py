
from bs4 import BeautifulSoup
from bs4.element import Comment
import requests
import urllib.request
import unicodedata
import json

measurements = ["tablespoons", "teaspoons", "pounds", "cups", "cans", "packages", "jars", "ounces", "containers", "bushels", "tons", \
    "tablespoon", "teaspoon", "pound", "cup", "can", "package", "jar", "ounce", "container", "bushel", "ton"]

# {
#     ingredients: {
#         groundbeef: {
#             quantity: 
#             measurement: 
#             additional_instructions: 
#             food_group:
#         }
#     }
# }

def createJSON(ingredients, quantities, more_directions):
    final = {}
    final['ingredients'] = {}
    for idx, i in enumerate(ingredients):
        final["ingredients"][i] = {}
        final["ingredients"][i]['quantity'] = quantities[idx]
        final['ingredients'][i]['additional_directions'] = more_directions[idx]
        final["ingredients"][i]['food_group'] = 'N/A'


    # final['ingredients'] = ingredients
    # final['quantities'] = quantities
    # final['directions'] = directions
    with open('recipe.json', 'w') as f:
        json.dump(final, f)


def parse(url):
    # parse website url
    webpage = requests.get(url, timeout=5)
    doc = BeautifulSoup(webpage.text, "html.parser")

    # get ingredients
    ingredients = []
    ingredientParse = doc.find_all("span", {"class": 'ingredients-item-name'})
    for element in ingredientParse: 
        ingredients.append(element.text)
    quantities = []
    parsed_ingredients = []
    add_direct = []
    for ingredient in ingredients:
        ingredient
        quantity = []
        ingredient_name = ""

        # find alternate quantities
        alternateQuantity = ""
        if not (ingredient[0].isalpha() or ingredient[0] == " "):
            quantity = [unicodedata.numeric(ingredient[0])]
            ingredient = ingredient[1:]
            if "(" in ingredient:
                alternateQuantity = ingredient.split('(')[1].split(')')[0]
                # remove it from ingredient
                ingredient = ingredient.split('(')[0] + ingredient.split(')')[1]
            if alternateQuantity != "":
                quantity.append(alternateQuantity)
    
        if "," in ingredient:
            separated = ingredient.split(",")
            ingredient = separated[0]
            additional_directions = separated[1].strip()
            add_direct.append(additional_directions)
        else:
            add_direct.append('N/A')

        check = 0
        for measurement in measurements:
            if measurement in ingredient:
                check = 1

                quantity[0] = str(quantity[0]) + " " + measurement
                ingredient_name = ingredient.split(measurement)[1].strip()
                parsed_ingredients.append(ingredient_name.strip())
                print(quantity[0])
                print(ingredient_name)
                break
        if not check:
            parsed_ingredients.append(ingredient.strip())
        
        quantities.append(quantity)

    print(parsed_ingredients)
    print(quantities)

    # get directions
    directions = []
    instructions = doc.find_all("div", {"class": 'paragraph'})
    for i in instructions:
        # print(i.p.text)
        directions.append(i.p.text)

    createJSON(parsed_ingredients, quantities, add_direct)
    return ingredients, quantities, directions