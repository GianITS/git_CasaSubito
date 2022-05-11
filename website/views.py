from flask import Blueprint, Flask, render_template
from flask_pymongo import PyMongo
import certifi
from .models import properties_collection

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
    return render_template('clients.html')

@views.route('/Immobili')
def properties():
    return render_template('properties.html')

@views.route('/RichiesteImmobiliari')
def properties_request():
    return render_template('properties_request.html')

if __name__ == "__main__":
    query = properties_collection.find({})
    for x in query:
        print(x)