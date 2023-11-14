from flask import Flask
from flask_restx import Api
from .utils import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from .service.event import event_namespace
from .service.auth import auth_namespace
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dd_jhkuywtw31200'
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///invent.db'
    app.config['JWT_SECRET_KEY'] = 'dd_jhlllywtw31200'

    db.init_app(app)
    with app.app_context():
        db.create_all()
    JWTManager(app)
    Migrate(app, db)
    CORS(app)

    api = Api(app, title="Inventory Management System", version='1.0')
    api.add_namespace(event_namespace, path='/api')
    api.add_namespace(auth_namespace, path='/api/auth')

    return app
