import json


class Recipe:
    def __init__(self, name, ingedients):
        self.name = name
        self.ingredients = ingedients


class Ingedient:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount


ipFile = 'kk.txt'
f = open(ipFile)
data = json.load(f)
outlets = data['machine']['outlets']['count_n']
quantities = data['machine']['total_items_quantity']
recipies = data['machine']['beverages']
r = recipies.dumps
for k, v in json.load(r):
    print(k, "-r-", v)

