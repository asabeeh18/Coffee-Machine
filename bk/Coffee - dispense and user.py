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


def quantity_check(beverage):
    for k in recipes[beverage]:
        if k not in quantities or quantities[k] < recipes[beverage][k]:
            return False,k
    return True,None


def dispense(beverage):
    # lock
    a,item = quantity_check(beverage)
    if not a:
        print(beverage, " NOT AVAILABLE, Low on ", item)
        return
    for k in recipes[beverage]:
        quantities[k] -= recipes[beverage][k]
    print(k, " Dispensed")
    # unlock


def user_menu():
    i = 1
    user_dict = {}
    # User Menu
    for k in recipes:
        a,item = quantity_check(k)
        if not a:
            print(i, ".", k, " NOT AVAILABLE, Low on ",item)
        else:
            print(i, ".", k)
        user_dict[i] = k
        i += 1
    sel = input()
    if not isinstance(sel, int):
        print("Only number allowed")
        # try again
    elif sel<1 or sel>=i:
        print("No such selection, Please enter in range of ", 1, "to ", (i - 1))
    else:
        # recipes[user_dict[sel]]
        dispense(user_dict[sel])


def initmachine(confFile):
    global quantities
    global recipes
    with open(ipFile, 'r') as myfile:
        data = myfile.read()
    data = json.loads(data)
    outlets = data['machine']['outlets']['count_n']
    quantities = data['machine']['total_items_quantity']
    recipes = data['machine']['beverages']
    # print(recipes['hot_tea'])
    # print(recipes['black_tea'])
    pass
    while True: user_menu()


ipFile = 'kk.txt'
initmachine(ipFile)
