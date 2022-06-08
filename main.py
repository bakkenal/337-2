import sys
from parse import parse, parseRest
from transform import doubleQuantity, from_vegetarian, to_vegetarian, from_healthy, to_healthy, to_chinese, to_indian

def printHelp():
    print("\n\nCS337 project - recipe parser")
    print("Input 1 - transformation. Options are: \n\
            vegetarian\n\
            healthy\n\
            quantity\n\
            style - chinese, indian\n\
Input 2 - to or from the transformation but in the case of 'quantity' transformation add double as the 2nd input\n\
Input 3 - the url to be transformed\n\n\
An example input could be \"python main.py vegetarian to [url]\"\n\
Since some modes, like style, transform to a url, use the cuisine instead of \"to\" or \"from\".\
For example - \"python main.py style chinese [url]\"\n\n")
    quit()

if len(sys.argv) != 4:
    # print help statement
    printHelp()

arguments = sys.argv[1:]
# print(arguments)
for i in range(len(arguments)):
    arguments[i] = arguments[i].lower()
transform = arguments[0]
mode = arguments[1]
url = arguments[2]

styles = ["chinese","indian"]

ingredients, quantities, directions, json = parse(url)
# stepsDict = parseRest(directions, ingredients)

# apply transformation
if transform == "vegetarian":
    if mode == "from":
        print("making " + url + " have meat")
        from_vegetarian(ingredients, json)
    if mode == "to":
        print("making " + url + " be vegetarian")
        to_vegetarian(ingredients, json)
    pass
elif transform == "healthy":
    if mode == "from":
        print("making " + url + " more unhealthy")
        from_healthy(json)
    if mode == "to":
        print("making " + url + " more healthy")
        to_healthy(json)
    pass
elif transform == "style":
    for style in styles:
        if mode == style:
            print("making " + url + " " + style)
            # something
            if mode == "chinese":
                to_chinese(ingredients, json)
            elif mode == "indian":
                to_indian(ingredients, json)
    pass
elif transform == 'quantity':
    if mode == 'double':
        print("making " + url + " double the quantity")
        doubleQuantity(json)
else:
    printHelp()


