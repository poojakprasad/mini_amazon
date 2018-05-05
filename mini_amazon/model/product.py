from pymongo import MongoClient
import re
from bson.objectid import ObjectId
import json

class Product :
    def __init__(self,name,description,price):
        self.name = name
        self.description = description
        self.price = price

class MongoProduct :


    def __init__(self):
        config = json.load(open('./config.json', 'r'))
        client = MongoClient(config['mongo_host'], config['mongo_port'])
        self.db = client[config['mongo_db_name']]



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


    def delete_by_id(self, _id):
        self.db.products.delete_one({'_id': ObjectId(_id)})


    def update_by_id(self,_id,updated_product):
        condition = dict()
        condition['_id'] = ObjectId(_id)
        self.db.products.update_one(filter=condition, update={'$set': updated_product})

    def get_product_list_from_product_ids(self, matched_ids):
        matches = []
        if(matched_ids is not None):
            for matched_id in matched_ids:
                matches.append(self.db.products.find_one({'_id': ObjectId(matched_id)}))
        return matches

    def add_stuff(self):
        for i in range(10):
            product = dict()
            product['name'] = "name" + str(i)
            product['description'] = "description" + str(i)
            product['price'] = "10" + str(i)
            self.db.products.insert_one(product)

