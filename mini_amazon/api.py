from mini_amazon.model.product import MongoProduct
from mini_amazon.model.user import MongoUser

from mini_amazon import app
from flask import request, Response , render_template,send_from_directory

mongo_product = MongoProduct()
mongo_user = MongoUser()

@app.route('/health', methods=['GET'])
def health():
    return 'healthy'


@app.route('/api/products', methods=['POST', 'GET'])
def products():
    if request.method == 'GET':
        query = request.args['name']
        userId = request.args['user_id']
        matches = mongo_product.search_by_name(query)
        #print("1")

        output_type = request.args.get('output_type', None)
        if output_type == 'html':
            #print("2")
            return render_template('results.html', query=query, results=matches, user_id=userId)
        else :
            return Response(str(matches), mimetype='application/json', status=200)


    elif request.method == 'POST':
        if request.form['op_type'] == 'insert':

            product = dict()
            product['name'] = request.form['name']
            product['description'] = request.form['description']
            product['price'] = request.form['price']
            mongo_product.save(product)
            # db.products.insert_one(product)

            return Response(str({'status': 'success'}), mimetype='application/json', status=200)

        elif request.form['op_type'] == 'delete':
            _id = request.form['_id']

            mongo_product.delete_by_id(_id)
            return Response(str({'status': 'success'}), mimetype='application/json', status=200)


        elif request.form['op_type'] == 'update':
            condition = dict()
            _id = request.form['_id']

            updated_prod = dict()
            if request.form['name'] != '':
                updated_prod['name'] = request.form['name']

            if request.form['description'] != '':
                updated_prod['description'] = request.form['description']

            if request.form['price'] != '':
                updated_prod['price'] = request.form['price']

            # db.products.update_one(filter=condition, update = {'$set': prod})
            mongo_product.update_by_id(_id, updated_prod)

            return Response(str({'status': 'updated'}), mimetype='application/json', status=200)



@app.route('/api/user', methods=['POST'])
def user():
    if request.form['op_type'] == "login" :
        username = request.form.get('username')
        password = request.form.get('password')

        is_valid = mongo_user.authenticate(username,password)

        if is_valid :
            name = mongo_user.get_name_by_username(username)
            userId = mongo_user.get_id_by_username(username)
            return render_template('profile.html',name= name,login_msg = "Welcome", user_id=userId)
        else :
            return render_template('index.html',message = "Invalid username/passsword")


    elif request.form['op_type'] == "signup" :
        user = dict()

        user['username'] = request.form.get('username')
        user['name'] = request.form.get('name')
        user['email']= request.form.get('email')
        user['password'] = request.form.get('password')
        user['cart'] = []

        does_exist = mongo_user.check_for_user_exist(request.form.get('username'))

        if does_exist:
            return render_template('index.html', user_exist_msg="Username exists, please enter a different username")
        else:
            mongo_user.save(user)
            return Response(str({"status": "user added"}), mimetype='application/json', status=200)

    else :
        return Response(str({"status" : "Invalid operation"}), mimetype='application/json', status=400)

@app.route('/api/cart', methods=['POST','GET'])
def cart():
    if request.form.get('op_type') == 'getcart':
        return get_all_cart_objects()

    elif request.args.get('op_type') == 'delete':
        userId = request.args.get('user_id')
        productId = request.args.get('product_id')
        matches = mongo_user.remove_prod_from_cart(userId, productId)
        return get_all_cart_objects()

    else:
        user_id = request.form.get('user_id',None)
        product_id = request.form.get('product_id', None)

        user= mongo_user.get_by_id(user_id)
        success = mongo_user.add_to_cart(user_id,product_id)
        user_data = mongo_user.get_by_id(user_id)

        return render_template('profile.html',name=user_data['name'],user_id=user_id)


def get_all_cart_objects():
    userId = request.args.get('user_id')
    if(userId is None):
        userId = request.form.get('user_id')
    matched_ids = mongo_user.get_usercart_by_userid(userId)
    matches = mongo_product.get_product_list_from_product_ids(matched_ids)
    return render_template('cart.html', user_id=userId, results=matches)

@app.route('/addStuff', methods=['GET'])
def add_stuff():
   mongo_product.add_stuff()
   return Response(str({'status': 'success'}), mimetype='application/json', status=200)