from flask import Flask
app = Flask(__name__,
 static_folder = './public',
 template_folder="./static")

from templates.code.views import index_blueprint
# register the blueprints
app.register_blueprint(index_blueprint)
