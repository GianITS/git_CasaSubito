from flask import Blueprint, Flask, render_template
from flask_pymongo import PyMongo
import certifi
from .models import clients_collection, properties_collection

views = Blueprint('views', __name__)

# PyMongo ---------------------------------------------------------------------
app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb+srv://GianITS:ProjectITS33@clusterits.do6lt.mongodb.net/Agenzia_Immo?retryWrites=true&w=majority"
mongo = PyMongo(app, tlsCAFile=certifi.where())


@views.route('/HomePage')
def home():
    return render_template('homepage.html')

@views.route('/Clienti')
def clients():
    clienti = list(clients_collection.find({},{"_id":0}))
    return render_template('clients.html', clienti=clienti)

@views.route('/Inserimento_Clienti')
def insert_clients():
    return render_template('insert_clients.html')

@views.route('/Immobili')
def properties():
    immobili = list(properties_collection.find({},{"_id":0}))
    return render_template('properties.html', immobili=immobili)

@views.route('/Inserimento_Immobili')
def insert_properties():
    return render_template('insert_properties.html')

@views.route('/RichiesteImmobiliari')
def properties_request():
    return render_template('properties_request.html')

if __name__ == "__main__":
    query = clients_collection.find({})
    for x in query:
        print(x)