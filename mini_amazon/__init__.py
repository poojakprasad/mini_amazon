from flask import Flask


app = Flask('mini_amazon',
            static_url_path='',
            template_folder = './templates',
            static_folder = './static')

from mini_amazon import views, api
