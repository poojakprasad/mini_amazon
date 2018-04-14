from flask import Flask, send_from_directory, request, Response
import pymongo
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.amazon

app = Flask('mini-amazon', static_url_path='')



@app.route('/health', methods=['GET'])
def health():
    return 'healthy'


@app.route('/', methods=['GET'])
def index():
    return send_from_directory('static', 'index.html')


@app.route('/api/products', methods=['POST', 'GET'])
def products():
    if request.method == 'GET':
        matching_prods = db.products.find({'name': {'$regex' : request.args['name'] }})
        matches = []
        for prods in matching_prods :
            matches.append(prods)
        return Response(str(matches),mimetype='application/json', status= 200)

    elif request.method == 'POST' :

        product = dict()
        product['name'] = request.form['name']
        product['description'] = request.form['description']
        product['price'] = request.form['price']

        db.products.insert_one(product)

        return Response(str({'status':'success'}), mimetype='application/json',status = 200)

@app.route('/all', methods = ['GET'])
def displayall():
    prods = db.products.find()
    matches = []
    for prod in prods:
        matches.append(prod)
    return Response(str(matches), mimetype='application/json', status=200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
