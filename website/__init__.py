from flask import Flask
from pymongo import MongoClient
import certifi

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ProjectITS33'

    # cluster = MongoClient("mongodb+srv://GianITS:ProjectITS33@clusterits.do6lt.mongodb.net", tlsCAFile=certifi.where())
    # db = cluster['Agenzia_Immo']
    # clients_collection = db['Clienti']
    # properties_collection = db['Immobili']
    # agents_collection = db['Agenti']

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    return app