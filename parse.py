
from bs4 import BeautifulSoup
from bs4.element import Comment
import requests
import urllib.request
import unicodedata
import json
import re

measurements = ["tablespoons", "teaspoons", "pounds", "cups", "cans", "packages", "jars", "ounces", "containers", "bushels", "tons", \
    "tablespoon", "teaspoon", "pound", "cup", "can", "package", "jar", "ounce", "container", "bushel", "ton"]

TIME = ['seconds', 'minutes', 'hours']

ALLMETHODS = ['bake', 'sear', 'stir fry', 'sautee', 'broil', 'fry', 'scortch', 'slow cook',
    'cook', "boil", "simmer", "grill", "grilled", 'stir in', 'stir', 'mix in', 'mix', 'chop',
    'slice', 'flip', 'whisk', 'devein', 'julienne', 'score', 'combine', 'melt', 'punch down', 'heat',
    'reduce', 'pour', 'skin', 'skim', 'dissolve', 'shape', 'drain', 'discard', 'blend', 'sprinkle',
    'uncover','cover', 'drain']

cooking_methods = ['stir in', 'stir', 'mix in', 'mix', 'chop',
    'slice', 'flip', 'whisk', 'devein', 'julienne', 'score', 'combine', 'melt', 'punch down', 'heat',
    'reduce', 'pour', 'skin', 'skim', 'dissolve', 'shape', 'drain', 'discard', 'blend', 'sprinkle',
    'uncover','cover']


TOOLS = ['oven', 'stove','broiler','gas grill','charcoal grill','grill',
         'toaster','rice cooker','pressure cooker','slow cooker','fryer',
         'blender','food processor','bowl','mixer','mandoline','spiralizer',
         'pot','pan','baking sheet','sheet','skillet','colander','saucepan',
         'aluminum foil','baking paper','wax paper','baking tin']


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

def toolsandmethods(arr, step):
    res = []
    for element in arr:
        if element in step:
            res.append(element)
    return res


def parseRest(directions, ingredients):
    rawSteps = directions #too lazy to change it 
    TimeSteps = []
    for step in rawSteps:
        #parsing for the time
        stepdict = {}
        directions = re.sub(r'[!?\.,\'\":()]+', '', step.lower()).split()
        steps = []
        for interval in TIME:
            if interval in directions: 
                idx = [i for i, x in enumerate(directions) if x == interval]
                for element in idx: 
                    if directions[element-2] == 'to' or directions[element-2] == '-':
                        speceficTimeStep =  directions[element-3] + ' ' + directions[element-2] + ' ' + directions[element-1] + ' ' + directions[element]
                    else:
                        speceficTimeStep = directions[element-1] + ' ' + directions[element] #no shot element gets out of bounds from list
                    steps.append(speceficTimeStep)
        stepdict['time'] = steps
        
        #parsing for the tools 
        steptools = toolsandmethods(TOOLS, directions)
        stepdict['tools'] = steptools
        
        #parsing for methods 
        stepmethods = toolsandmethods(ALLMETHODS, directions)
        stepdict['methods'] = stepmethods
        
        #parsing for ingredients 
        ingredientmethods = toolsandmethods(ingredients, ' '.join(directions)) #have to take in a string instead of array because ingredients can be more than 2 words 
        stepdict['ingredients'] = ingredientmethods
        
        #also have the actual step for that instruction
        stepdict['direction'] = step
        
        TimeSteps.append(stepdict)
    print(TimeSteps)
    return TimeSteps
    