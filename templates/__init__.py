from flask import Flask
from flask_login import LoginManager

from templates.code.User import User
from templates.code.views import index_blueprint, PCM

app = Flask(__name__, static_folder = './public', template_folder="./static")

# register the blueprints
app.register_blueprint(index_blueprint)

login_manager = LoginManager()
login_manager.login_view = 'index.index'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return PCM.getUserByID(user_id)
