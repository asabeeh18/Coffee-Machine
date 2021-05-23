import json


class Recipe:
    def __init__(self, name, ingedients):
        self.name = name
        self.ingredients = ingedients


class Ingedient:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount


def initMachine(confFile):
    with open(ipFile, 'r') as myfile:
        data = myfile.read()
    data = json.loads(data)
    outlets = data['machine']['outlets']['count_n']
    quantities = data['machine']['total_items_quantity']
    recipies = data['machine']['beverages']
    

ipFile = 'kk.txt'
initMachine(ipFile)
