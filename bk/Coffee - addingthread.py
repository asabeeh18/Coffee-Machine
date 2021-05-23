import json
from threading import Thread


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
            return False, k
    return True, None


def refill_item():
    # Refill only possible when nobody else is dispensing
    # lock
    i = 1
    user_dict = {}
    for k in quantities:
        print(i, " ", k, ' is ', quantities[k])
        user_dict[i] = k
        i += 1

    print(i, ". Add new item")
    sel = take_input()
    if not sel.isnumeric():
        print("Only number allowed")
        # try again
    elif int(sel) < 1 or int(sel) > i:
        print("No such selection, Please enter in range of ", 1, "to ", (i - 1))
    else:
        sel=int(sel)
        if sel == i:
            print('Enter name: ')
            s = take_input()
            print('Enter Quantity: ')
            q = take_input()
            quantities[s] = int(q) #sanitise
        else:
            print('Add value: ')
            q = int(take_input()) #sanitise
            quantities[user_dict[sel]] += q
            print('New amount for ', user_dict[sel], ' is: ', quantities[user_dict[sel]])
    # unlock


def dispense(beverage):
    # lock
    a, item = quantity_check(beverage)
    if not a:
        print(beverage, " NOT AVAILABLE, Low on ", item)
        return
    for k in recipes[beverage]:
        quantities[k] -= recipes[beverage][k]
    print(k, " Dispensed")
    # unlock


def take_input():
    # sanitisation

    return input()


def user_menu():
    i = 1
    user_dict = {}
    # User Menu
    for k in recipes:
        a, item = quantity_check(k)
        if not a:
            print(i, ".", k, " NOT AVAILABLE, Low on ", item)
        else:
            print(i, ".", k)
        user_dict[i] = k
        i += 1
    print(i, ". Refill")
    sel = take_input()
    if not sel.isnumeric():
        print("Only number allowed")
        # try again
    elif int(sel) < 1 or int(sel) > i:
        print("No such selection, Please enter in range of ", 1, "to ", (i - 1))
    else:
        # recipes[user_dict[sel]]
        sel=int(sel)
        if sel is i:
            refill_item()
        else:
            dispense(user_dict[sel])


def initmachine(confFile):
    global quantities
    global recipes
    with open(confFile, 'r') as myfile:
        data = myfile.read()
    data = json.loads(data)
    outlets = data['machine']['outlets']['count_n']
    quantities = data['machine']['total_items_quantity']
    recipes = data['machine']['beverages']
    for i in range(outlets):
        thread = Thread(target=user_menu())
        thread.start()
    # print(recipes['hot_tea'])
    # print(recipes['black_tea'])
    pass
    while True: user_menu()

# ipFile = 'kk.txt'
# initmachine(ipFile)
