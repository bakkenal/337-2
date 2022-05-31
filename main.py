import sys
from parse import parse

def printHelp():
    print("\n\nCS337 project - recipe parser")
    print("Input 1 - transformation. Options are: \n\
            vegetarian\n\
            healthy\n\
            style - Italian or Chinese\n\
            optionals - \n\n\
Input 2 - to or from the transformation\n\
Input 3 - the url to be transformed\n\n\
An example input could be \"python script.py vegetarian to [url]\"\n\
Since some modes, like style, transform to a url, use the cuisine instead of \"to\" or \"from\".\
For example - \"python script.py style chinese [url]\"\n\n")
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

styles = ["chinese", "italian"]

ingredients, quantities, directions = parse(url)

# apply transformation
if transform == "vegetarian":
    if mode == "from":
        print("making " + url + " have meat")
    if mode == "to":
        print("making " + url + " be vegetarian")
    pass
elif transform == "healthy":
    if mode == "from":
        print("making " + url + " more unhealthy")
    if mode == "to":
        print("making " + url + " more healthy")
    pass
elif transform == "style":
    for style in styles:
        if mode == style:
            print("making " + url + " " + style)
            # something
    pass
elif transform == "optionals":
    print("TODO: determine these")
    pass
else:
    printHelp()


