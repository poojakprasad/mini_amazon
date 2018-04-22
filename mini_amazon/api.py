from mini_amazon.model.product import MongoProduct
from mini_amazon.model.user import MongoUser

from mini_amazon import app
from flask import request, Response , render_template

mongo_product = MongoProduct()
mongo_user = MongoUser()

@app.route('/health', methods=['GET'])
def health():
    return 'healthy'


@app.route('/api/products', methods=['POST', 'GET'])
def products():
    if request.method == 'GET':
        query = request.args['name']
        matches = mongo_product.search_by_name(query)
        #print("1")

        output_type = request.args.get('output_type', None)
        if output_type == 'html':
            #print("2")
            return render_template('results.html', query=query, results=matches)
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


@app.route('/api/users', methods=['POST', 'GET', 'DELETE'])
def users():
    if request.method == 'GET':
        matches = mongo_user.search_by_name(request.args['name'])
        return Response(str(matches), mimetype='application/json', status=200)

        query = {
            'name': re.compile(request.args['name'], re.IGNORECASE)
        }
        matching_users = db.users.find(query)
        matches = []
        for users in matching_users:
            matches.append(users)
        return Response(str(matches), mimetype='application/json', status=200)

    elif request.method == 'POST':
        if request.form['op_type'] == 'insert':

            user = dict()
            user['name'] = request.form['name']
            user['user_name'] = request.form['user_name']
            user['password'] = request.form['password']
            mongo_user.save(user)
            # db.users.insert_one(user)

            return Response(str({'status': 'success'}), mimetype='application/json', status=200)

        elif request.form['op_type'] == 'delete':
            id = request.form['_id']

            mongo_user.delete(id)
            return Response(str({'status': 'success'}), mimetype='application/json', status=200)

        elif request.form['op_type'] == 'update':
            condition = dict()
            _id = request.form['_id']

            updated_user = dict()
            if request.form['name'] != '':
                updated_user['name'] = request.form['name']

            if request.form['user_name'] != '':
                updated_user['user_name'] = request.form['user_name']

            if request.form['password'] != '':
                updated_user['password'] = request.form['password']

            # db.users.update_one(filter=condition, update = {'$set': user})
            mongo_user.update_by_id(_id, updated_user)

            return Response(str({'status': 'updated'}), mimetype='application/json', status=200)
