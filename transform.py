import json
import pprint
meat = ['chicken', 'meat', 'beef', 'steak', 'pork', 'turkey', 'tuna', 'salmon', 'halibut', 'octopus', 'ground beef', 'veal',
       'chorizo', 'pepperoni', 'lobster', 'shrimp', 'bacon', 'turkey bacon', 'crab', 'ham']

primary_methods = ['bake', 'sear', 'stir fry', 'sautee', "saute", 'broil', 'fry', 'scorch', 'slow cook',
    'cook', "boil", "simmer", "grill", "grilled", "roast", "deep fry", "steam"]

healthy_map = { "fry" : "bake",
                "deep fry" : "bake",
                "roast" : "bake",
                "boil" : "steam",
                "bake" : "boil", 
                "Fry" : "Bake",
                "Deep fry" : "Bake",
                "Roast" : "Bake",
                "Boil" : "Steam",
                "Bake" : "Boil"}
unhealth_map = {"bake" : "fry",
                "sear" : "fry",
                "stir fry" : "fry",
                "sautee" : "fry",
                "saute" : "fry",
                "boil" : "fry",
                "broil" : "fry",
                "steam" : "fry", 
                "Bake" : "Fry",
                "Sear" : "Fry",
                "Stir fry" : "Fry",
                "Sautee" : "Fry",
                "Saute" : "Fry",
                "Boil" : "Fry",
                "Steam" : "Fry",
                "Broil" : "Fry"}

#transform JSON 
def transformJSON(dictionary, switch):
    for key in switch.keys():
        #maybe should change additional directions and quantity but who cares 
        dictionary['ingredients'][switch[key]] = dictionary['ingredients'][key]
    for step in dictionary['steps']:
        for key in switch.keys():
            if key in step['ingredients']:
                idx = step['ingredients'].index(key)
                step['ingredients'][idx] = switch[key]
                new_directions = step['direction'].replace(key, switch[key])
                step['direction'] = new_directions
    for key in switch.keys():
        del dictionary['ingredients'][key]

    # dictionary['Recipe_Title'] = 'Vegetarian ' + dictionary['Recipe_Title']
    return dictionary

def storeJSON(dictionary, str):
    with open(f'{str} recipe.json', 'w') as f:
        json.dump(dictionary, f)


def to_vegetarian(I, J): #might not take in url as variable
    vegetarian_ingredients = []
    switch_ingredients = {}
    for i in I:
        i = i.lower()
        ingredient_has_meat = False
        for m in meat:
            #if there is a protein 
            if m in i:
                ingredient_has_meat = True
                #check if it is a soup 
                if 'stew' in i or 'broth' in i or 'stock' in i:
                    new = 'vegetable stock'
                    vegetarian_ingredients.append(new)
                    switch_ingredients[i] = new
                #not it is not a soup
                else:
                    new = 'tofu'
                    vegetarian_ingredients.append(new)
                    switch_ingredients[i] = new
                break #break because of the edge condition beef stew meat so it looped twice becuz of 'beef' and 'meat' 
        if ingredient_has_meat == False:
            vegetarian_ingredients.append(i)
    if switch_ingredients:
        vegetarian = transformJSON(J, switch_ingredients) #this actually changes the original json so theres no deep copy 
        storeJSON(vegetarian, 'Transformed vegetarian')
        prettyPrint(vegetarian)
    else:
        print('THIS RECIPE IS ALREADY VEGETARIAN!!!')

def from_vegetarian(ingredient, J):
    #check if a dish is vegetarian or not
    is_meat = False
    for i in ingredient:
        i = i.lower()
        for m in meat:
            if m in i:
                is_meat = True #there is a meat 
                break
    if is_meat:
        print('THIS RECIPE IS NOT VEGETARIAN!!!')
    else:
        J['ingredients']['bacon'] = {}
        J['ingredients']['bacon']['quantity'] = '4 sticks'
        J['ingredients']['bacon']['additional_directions'] = 'crushed'
        J['ingredients']['bacon']['food_group'] = 'N/A'
        step = {
            'time':[],
            'tools': [],
            'methods': [],
            'ingredients': ['bacon'],
            'direction': 'Crush the sticks of bacon into bacon bits and sprinkle it on top of your dish.'
        }
        J['steps'].append(step)
        storeJSON(J, 'Non-vegetarian')
        prettyPrint(J)

def to_healthy(J):
    # go through step by step and replace with mapped method in dicts
    for step in J['steps']:
        print(step)
        for i, method in enumerate(step['methods']):
            if method in healthy_map:
                step['methods'][i] = healthy_map[method]
        for i, method in enumerate(step['primary_method']):
            if method in healthy_map:
                step['primary_method'][i] = healthy_map[method]
        direction = step['direction'].split(" ")
        #print(direction)
        for i, word in enumerate(direction):
            if word in healthy_map:
                direction[i] = healthy_map[word]
        new_thing = ' '.join(direction)
        step['direction'] = new_thing
        #print(step['direction'])
    storeJSON(J, "Healthy")
    prettyPrint(J)


def from_healthy(J):
    for step in J['steps']:
        for i, method in enumerate(step['methods']):
            if method in unhealth_map:
                step['methods'][i] = unhealth_map[method]
        for i, method in enumerate(step['primary_method']):
            if method in unhealth_map:
                step['primary_method'][i] = unhealth_map[method]
        direction = step['direction'].split(" ")
        #print(direction)
        for i, word in enumerate(direction):
            if word in unhealth_map:
                direction[i] = unhealth_map[word]
        new_thing = ' '.join(direction)
        step['direction'] = new_thing
    storeJSON(J, "Unhealthy")
    prettyPrint(J)

def to_chinese(ingredient, J):
    if 'soy sauce' not in ingredient:
        J['ingredients']['soy sauce'] = {}
        J['ingredients']['soy sauce']['quantity'] = 'N/A'
        J['ingredients']['soy sauce']['additional_directions'] = 'N/A'
        J['ingredients']['soy sauce']['food_group'] = 'N/A'
        step = {
            'time':[],
            'tools':[],
            'methods':[],
            'ingredients':['soy sauce'],
            'direction': 'Sprinkle on soy sauce to taste'
        }
        J['steps'].append(step)
        storeJSON(J, "Chinese")
        prettyPrint(J)
    else:
        print("THIS DISH IS ALREADY CHINESE")
        
def to_indian(ingredient, J):
    if 'curry' not in ingredient:
        J['ingredients']['curry'] = {}
        J['ingredients']['curry']['quantity'] = 'N/A'
        J['ingredients']['curry']['additional_directions'] = 'N/A'
        J['ingredients']['curry']['food_group'] = 'N/A'
        step = {
            'time':[],
            'tools':[],
            'methods':[],
            'ingredients':['curry'],
            'direction': 'Sprinkle on curry to taste'
        }
        J['steps'].append(step)
        storeJSON(J, "Indian")
        prettyPrint(J)
    else:
        print("THIS DISH IS ALREADY INDIAN")

def doubleQuantity(J):
    for ingredient in J['ingredients']:
        new_quantity = []
        for q in J['ingredients'][ingredient]['quantity']:
            if type(q) == int or type(q) == float:
                new_quantity.append(q*2)
            elif type(q) == str:
                if isfloat(q.split()[0]):
                    num = float(q.split()[0])
                    changed = str(num*2) + ' ' + ' '.join(q.split()[1:])
                    new_quantity.append(changed)
        J['ingredients'][ingredient]['quantity'] = new_quantity
    storeJSON(J, "Double")
    prettyPrint(J)

def prettyPrint(input):
    pprint.pprint(input)

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False