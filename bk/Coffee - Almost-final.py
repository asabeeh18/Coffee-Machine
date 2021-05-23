import json
import threading
import time

recipes = {}
quantities = {}
lock = threading.Lock()

def printr(l):
    s=''.join(map(str, l))
    print(s,file=open("output.txt", "a"))

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
        printr(["Only number allowed"])
        # try again
    elif int(sel) < 1 or int(sel) > i:
        printr(["No such selection, Please enter in range of ", 1, "to ", (i - 1)])
    else:
        sel = int(sel)
        if sel == i:
            print('Enter name: ')
            s = take_input()
            if s in quantities:
                printr([s, ' is already present Invalid input!'])
                return
            print('Enter Quantity: ')
            q = take_input()
            # quantities[s] = int(q) #sanitise
            add_ingred(s, q)
        else:
            print('Add value: ')
            q = int(take_input())  # sanitise
            change_quantity(user_dict[sel], q)
            # quantities[user_dict[sel]] += q
            printr(['New amount for ', user_dict[sel], ' is: ', quantities[user_dict[sel]]])
    # unlock


def add_ingred(name, qt):
    with lock:
        quantities[name] = qt
        time.sleep(5)


def change_quantity(ingred, amt):
    if not lock.acquire(blocking=False):
        #print('Waiting for lock...')
        lock.acquire()
        #print('Acquired!')
    try:
        quantities[ingred] += amt
        time.sleep(2)
    finally:
        lock.release()
#with lock:
    #    quantities[ingred] += amt
    #    time.sleep(2)


def dispense(beverage):
    # lock
    a, item = quantity_check(beverage)
    if not a:
        printr([beverage, " NOT AVAILABLE, Low on ", item])
        return False
    for k in recipes[beverage]:
        change_quantity(k, -recipes[beverage][k])
        # quantities[k] -= recipes[beverage][k]
    return True


def take_input():
    # sanitisation
    return input()


def user_menu(outlet_num):
    # outlet_num=outlet_num[0]
    while True:
        printr(['Taking from Outlet ', outlet_num])
        i = 1
        user_dict = {}
        # User Menu
        for k in recipes:
            a, item = quantity_check(k)
            if not a:
                printr([i, ".", k, " NOT AVAILABLE, Low on ", item])
            else:
                print(i, ".", k)
            user_dict[i] = k
            i += 1
        print(i, ". Refill")
        sel = take_input()
        if sel is 'kill_thread':  #for test
            printr(['Thread Killed'])
            return
        if not isinstance(sel,int) and not sel.isnumeric():
            printr(["Only number allowed"])
            # try again
        elif int(sel) < 1 or int(sel) > i:
            printr(["No such selection, Please enter in range of ", 1, "to ", (i - 1)])
        else:
            # recipes[user_dict[sel]]
            sel = int(sel)
            if sel is i:
                refill_item()
            else:
                if dispense(user_dict[sel]):
                    printr([user_dict[sel], " Dispensed from outlet", outlet_num])


def initmachine(confFile):
    global quantities
    global recipes
    with open(confFile, 'r') as myfile:
        data = myfile.read()
    data = json.loads(data)
    outlets = data['machine']['outlets']['count_n']
    quantities = data['machine']['total_items_quantity']
    recipes = data['machine']['beverages']
    thread = []
    for i in range(outlets):
        thread.append(threading.Thread(target=user_menu, args=([i])))
        thread[-1].start()

    for thr in thread:
        thr.join()
    # print(recipes['hot_tea'])
    # print(recipes['black_tea'])
    # while True: user_menu()

# ipFile = 'kk.txt'
# initmachine(ipFile)
