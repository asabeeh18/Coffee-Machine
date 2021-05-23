import json


class Recipe:
    def __init__(self, name, ingedients):
        self.name = name
        self.ingredients = ingedients

recipes = {}
quantities = {}
class Ingedient:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

def quantity_check(ingred):
    return False

def dispense(beverage):
    #lock
    for k in recipes[beverage]:
        quantities[k]-=recipes[beverage][k]
    print(k," Dispensed")
    #unlock

def initMachine(confFile):
    global quantities
    global recipes
    with open(ipFile, 'r') as myfile:
        data = myfile.read()
    data = json.loads(data)
    outlets = data['machine']['outlets']['count_n']
    quantities = data['machine']['total_items_quantity']
    recipes = data['machine']['beverages']
    #print(recipes['hot_tea'])
    #print(recipes['black_tea'])
    pass
    i=1
    user_dict={}
    #User Menu
    for k in recipes:
        if not quantity_check(recipes[k]):
            print(i, ".", k," NOT AVAILABLE")
        else:
            print(i,".",k)
        user_dict[i]=k
        i+=1
    sel=input()
    if not isinstance(sel,int):
        print("Only number allowed")
        #try again
    elif 0>sel>=i:
        print("No such selection, Please enter in range of ",1,"to ",(i-1))
    else:
        #recipes[user_dict[sel]]
        dispense(user_dict[sel])



ipFile = 'kk.txt'
initMachine(ipFile)
