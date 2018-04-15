from pymongo import MongoClient
import re

class Product :
    def __init__(self,name,description,price):
        self.name = name
        self.description = description
        self.price = price

class MongoProduct :

    def __init__(self):
        client = MongoClient('localhost', 27017)
        db = client.amazon



    def save(self,product):
        self.db.products.insert_one(product)



    def search_by_name(self,name):
        query = {
            'name': re.compile(name, re.IGNORECASE)
        }
        matching_prods = self.db.products.find(query)
        matches = []
        for prods in matching_prods:
            matches.append(prods)
         return  matches


    def delete_by_id(self,_id):
        self.db.products.delete_one({'_id': _id})


    def update_by_id(self,_id,updated_product):
        condition = dict()
        condition['_id'] = _id
        self.db.products.update_one(filter=condition, update={'$set': prod})