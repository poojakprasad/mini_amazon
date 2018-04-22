from flask import send_from_directory
from mini_amazon import app


@app.route('/', methods=['GET'])
def index():
    #print('abc')
    return send_from_directory('./static', 'index.html')



