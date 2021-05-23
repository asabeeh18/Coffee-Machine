import json
import sys
import threading
import time

recipes = {}

# should only be updated with lock as multiple threads will be able to change this
quantities = {}
lock = threading.Lock()
print('Lock Created')


def quantity_check(beverage):
    """
    Function checks if the beverage can be made if not it returns the missing ingredients
    If the function returns False, None, None it should be inferred that the beverage in not present in the recipe list
    :param beverage: Indicates the beverage name for which quantity check is to be done
    :return:
        bool: Indicating the drink can be dispensed (This is not final as things may change during final dispensing due
                to other threads)
        list: List of ingredients which are less
        list: list of ingredients which are not present

    """
    miss = []
    low = []
    if beverage not in recipes:
        return False, None, None

    # Check if beverage can be made and update the missing ingredients if applicable
    for k in recipes[beverage]:
        if k not in quantities:
            miss.append(k)
        elif quantities[k] < recipes[beverage][k]:
            low.append(k)
    if len(miss) > 0 or len(low) > 0:
        return False, low, miss
    return True, None, None


def fill_new_item(name, qt):
    """
    Adds the new ingredient with some quantity
    :param name: Name of the new ingredient
    :param qt: Quantity to add for new ingredient
    :return: bool: True if ingredient is successfully added, False if the ingredient is not a new ingredient
    """
    with lock:
        if name in quantities:
            return False
        quantities[name] = qt
        time.sleep(5)
        return True


def change_quantity(ingred, amt):
    """
    Increments or decrements the quantity of an ingredient, is used for both refill and dispense functions
    :param ingred: Ingredient name
    :param amt: Amount to add or subtract
    :return: None
    """
    quantities[ingred] += amt


def print_deficiency(beverage, low, miss):
    """
    Prints appropriate user message to let user know why the beverage could not be made
    :param beverage: Beverage name
    :param low: List of ingredients we are low on
    :param miss: List of missing ingredients
    :return: None
    """
    if low is None and miss is None:
        print('No such beverage ', beverage)
    elif low is not None and len(low) > 0:
        print(beverage, ' cannot be prepared as ', low, ' is not sufficient')
    elif miss is not None and len(miss) > 0:
        print(beverage, ' cannot be prepared as ', miss, ' is not available')
    elif len(low) > 0 and len(miss) > 0:
        print(beverage, ' cannot be prepared as ', low, ' is not sufficient and ', miss, ' is not available')


def dispense(beverage):
    """
    Dispenses the drink for the user the entire functions needs to be mutually excluded
    :param beverage: beverage name
    :return:
        bool: Indicates if beverage was dispensed.
        list: List of ingredients which are less for the current beverage
        list: list of ingredients which are not present for the current beverage
    """
    try:
        lock.acquire()
        dispensable, low, miss = quantity_check(beverage)
        if not dispensable:
            print_deficiency(beverage, low, miss)
            return False, low, miss
        for recipe in recipes[beverage]:
            change_quantity(recipe, -recipes[beverage][recipe])
    finally:
        lock.release()
    print(beverage, ' is prepared')
    return True



def load_machine(confFile):
    """
    Load the machine with recipes, ingredient list and quantities and number of outlets
    :param confFile: Path to JSON file containing the configurable items
    :return: Number of outlets
    """
    global quantities
    global recipes
    with open(confFile, 'r') as myfile:
        data = myfile.read()
    data = json.loads(data)
    outlets = data['machine']['outlets']['count_n']
    quantities = data['machine']['total_items_quantity']
    recipes = data['machine']['beverages']
    return outlets


#========Functions below this line are needed only when using the user interface========

def take_input(outlet, var_type, lim):
    """
    Accepts the input form user and performs basic sanity check for integer values
    :param outlet: Outlet number from where input to take
    :param var_type: THe datatype to accept
    :param lim: ONly valid for integer, the max value to accept
    :return: data if it is proper, None if invalid data is entered
    """
    user_input = input(str(outlet).join('>'))
    # do some sanity bare minimum sanity checks
    if user_input.isnumeric() and isinstance(int(user_input), var_type):
        user_input = int(user_input)
        if 0 < user_input <= lim:
            return user_input
    elif isinstance(user_input, var_type):
        return user_input
    print('Invalid Input!!!')
    return None


def refill_item(outlet_num):
    """
    User menu to refill item
    :param outlet_num: OUtlet number from where this function is being accessed
    :return: None
    """
    i = 1
    # Use this dictionary to store the item number and the name, when user inputs a number
    user_dict = {}
    for k in quantities:
        print(i, " ", k, ' is ', quantities[k])
        user_dict[i] = k
        i += 1
    print(i, ". Add new item")

    sel = take_input(outlet_num, int, i)
    if sel is None:
        return

    if sel == i:
        # User selects to add new ingredient
        print('Enter name: ')
        s = take_input(outlet_num, str, 0)
        if s is None:
            return
        if s in quantities:
            print(s, ' is already present Invalid input!')
            return
        print('Enter Quantity: ')
        q = take_input(outlet_num, int, sys.maxsize)
        if q is None:
            return
        fill_new_item(s, q)
    else:
        # User selects to refill an ingredient
        print('Add value: ')
        q = take_input(outlet_num, int, sys.maxsize)
        if q is None:
            return
        change_quantity(user_dict[sel], q)
        print('New amount for ', user_dict[sel], ' is: ', quantities[user_dict[sel]])


def user_menu(outlet_num):
    """
    Initial User menu to list beverages or restock on ingredients
    :param outlet_num: The outlet number we are currently using
    :return: None
    """
    while True:
        print('===Taking from Outlet ', outlet_num, '===')
        i = 1
        # Use this dictionary to store the item number and the name, to identify the item when user inputs a number
        user_dict = {}
        # User Menu
        for k in recipes:
            a, low, miss = quantity_check(k)
            if not a:
                print_deficiency(k, low, miss)
            else:
                print(i, ".", k)
            user_dict[i] = k
            i += 1
        print(i, ". Refill")

        sel = take_input(outlet_num, int, i)

        if sel is i:
            # User selects to refill
            refill_item(outlet_num)
        else:
            if dispense(user_dict[sel]):
                print(user_dict[sel], " Dispensed from outlet", outlet_num)


def initmachine(confFile):
    """
    The starting function if we need to use the user menu instead of the testing functionality.
    Creates and starts threads for each outlet
    :param confFile: Path to JSON file containing the configurable items
    :return: None
    """
    outlets = load_machine(confFile)
    thread = []
    for i in range(outlets):
        thread.append(threading.Thread(target=user_menu, args=([i+1])))

        # So that the threads exit on ctrl+c
        thread[-1].daemon = True
        thread[-1].start()
    for thr in thread:
        # Wait to all threads
        thr.join()


"""
Uncomment the below code and run python Coffee.py to use the user menu functionality
ipFile is the path to JSON file containing the configurable items
"""
#ipFile = 'single_thread.txt'
#initmachine(ipFile)
