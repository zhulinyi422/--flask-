import os

import redis
from flask import Flask
from flask_session import Session
from App.user_views import user_blueprint
from App.models import db

def create_app():
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    static_dir = os.path.join(BASE_DIR,'static')
    templates_dir = os.path.join(BASE_DIR,'templates')
    app = Flask(__name__,static_folder=static_dir,template_folder=templates_dir)
    app.register_blueprint(blueprint=user_blueprint,url_prefix='/user')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:zly1995422@localhost:3306/my_flask'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'secret_key'
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port=6379)
    app.config['SESSION_KEY_PREFIX'] = 'flask'
    db.init_app(app=app)
    Session(app=app)
    return app


