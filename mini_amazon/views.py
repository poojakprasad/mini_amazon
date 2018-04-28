from flask import render_template
from mini_amazon import app


@app.route('/', methods=['GET'])
def index():
    #print('abc')
    return render_template('index.html')



