from pymongo import MongoClient
from bson.objectid import ObjectId
import json

class User :
    def __init__(self,name,_id,user_name, password):
        self.name = name
        self._id = _id
        self.user_name = user_name
        self.password = password


class MongoUser :


    def __init__(self):
        config = json.load(open('./config.json','r'))
        client = MongoClient(config['mongo_host'], config['mongo_port'])
        self.db = client[config['mongo_db_name']]



    def save(self,user):
        # user = {
        #     'name' : name ,
        #     'username' :username ,
        #     'email' : email ,
        #     'password' : password,
        #     'cart' : []
        # }
        self.db.users.insert_one(user)




    def authenticate(self,username,password):
        query = {
            'username' : username,
            'password' : password
        }
        cursor = self.db.users.find(query)
        if cursor is not None and cursor.count() > 0 :
            return True
        else:
            return False

    def get_name_by_username(self,username):
        cursor = self.db.users.find({'username':username})
        user_data = cursor[0] if cursor.count() > 0 else None
        if user_data is None:
            return "Anonymous"
        else:
            matches = []
            for user in cursor:
                matches.append(user)
            return matches[0]['name']


    def check_for_user_exist(self,username):
        cursor = self.db.users.find({'username': username})
        user_data = cursor[0] if cursor.count() > 0 else None
        if user_data is None:
            return False
        else:
            return True


    def add_to_cart(self,user_id,product_id):
        condition = {'_id' : ObjectId(user_id)}
        cursor = self.db.users.find(condition)
        user_data = cursor[0] if cursor.count() > 0 else None
        if user_data is None :
            return False

        if 'cart' not in user_data :
            user_data['cart'] = []

        if ObjectId(product_id) not in user_data['cart']:
            user_data['cart'].append(ObjectId(product_id))
            self.db.users.update_one(filter=condition, update={'$set':user_data})
        return True

    def get_by_id(self,_id):
        query = {
            '_id' : ObjectId(_id)
        }
        cursor = self.db.users.find(query)
        user = cursor[0] if cursor.count() > 0 else None
        return user

    def get_id_by_username(self, username):
        cursor = self.db.users.find({'username': username})
        user_data = cursor[0] if cursor.count() > 0 else None
        if user_data is None:
            return "Anonymous"
        else:
            matches = []
            for user in cursor:
                matches.append(user)
            return matches[0]['_id']

    def get_usercart_by_userid(self,user_id):
        user = self.get_by_id(user_id)
        return user['cart'] if user is not None else None


    def remove_prod_from_cart(self,user_id,product_id):
        try:
            condition = {'_id': ObjectId(user_id)}
            user = self.db.users.find_one({'_id': ObjectId(user_id)})
            cart = user['cart']
            cart.remove(ObjectId(product_id))
            self.db.users.update_one(filter=condition, update={'$set':{'cart':cart}})
        except:
            pass