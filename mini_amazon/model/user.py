from pymongo import MongoClient
import re
from bson.objectid import ObjectId
class User :
    def __init__(self,name,_id,user_name, password):
        self.name = name
        self._id = _id
        self.user_name = user_name
        self.password = password

class MongoUser :


    def __init__(self):
        client = MongoClient('localhost', 27017)
        db = client.amazon



    def save(self,user):
        self.db.users.insert_one(user)



    def search_by_name(self,name):
        query = {
            'name': re.compile(name, re.IGNORECASE)
        }
        matching_users = self.db.users.find(query)
        matches = []
        for user in matching_users:
            matches.append(user)
        return  matches


    def delete_by_id(self,_id):
        self.db.users.delete_one({'_id': _id})


    def update_by_id(self,_id,updated_user):
        condition = dict()
        condition['_id'] = ObjectId(_id)
        self.db.users.update_one(filter=condition, update={'$set': updated_user})