import sys
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import requests

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

def printHelp():
    print("\n\nCS337 project - recipe parser")
    print("Input 1 - transformation. Options are: \n\
            Vegetarian\n\
            Healthy\n\
            Style - Italian or Chinese\n\
            Optionals - \n\n\
Input 2 - to or from the transformation\n\
Input 3 - the url to be transformed\n\n\
An example input could be \"python script.py vegetarian to [url]\"\n\
Since some modes, like style, transform to a url, use the cuisine instead of \"to\" or \"from\".\
For example - \"python script.py style chinese [url]\"\n\n")
    quit()

def parseRecipe():
    pass

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

# parse website url
webpage = requests.get(url, timeout=5)
doc = BeautifulSoup(webpage.text, "html.parser")
# ingredients = doc.find_all("section", {"class": "recipeIngredients"})
# test = ingredients.find("ingredients-item")
ingredients = []
ingredientParse = doc.find_all("span", {"class": 'ingredients-item-name'})
print(ingredientParse)
for element in ingredientParse: 
    print(element.text)
    ingredients.append(element.text)

# html = urllib.request.urlopen('https://www.allrecipes.com/recipe/24074/alysias-basic-meat-lasagna/').read()
# print(text_from_html(html))

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


