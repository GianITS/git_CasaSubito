from flask import Blueprint, Flask, render_template ,flash, redirect, url_for
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

#inserimento nuovo cliente

from wtforms import StringField, SubmitField, RadioField, EmailField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

class FormInsertClient(FlaskForm):
    nome = StringField("Nome", [DataRequired()])
    cognome = StringField("Cognome", [DataRequired()])
    indirizzo = StringField("Indirizzo", [DataRequired()])
    citta = StringField("citta", [DataRequired()])
    cellulare = StringField("Cellulare", [DataRequired()])
    mail = EmailField("Email", [DataRequired()])
    azione = RadioField("azione", choices = ["Compra", "Vende"])
    submit = SubmitField("Inserisci")

@views.route('/Inserimento_Clienti', methods=["GET", "POST"])
def insert_clients():
    nome = ""
    cognome = ""
    indirizzo = ""
    citta = ""
    cellulare = ""
    mail = ""
    azione =""

    form=FormInsertClient()
    if form.validate_on_submit():
        nome = form.nome.data
        cognome = form.cognome.data
        indirizzo = form.indirizzo.data
        citta = form.citta.data
        cellulare = form.cellulare.data
        mail = form.mail.data
        azione = form.azione.data

        new_client = {"nome":nome, "cognome":cognome, "indirizzo":indirizzo, "citta":citta, "cellulare":cellulare, "mail":mail, "azione":azione}

        if clients_collection.find_one({"cellulare":cellulare},{}):
            flash("Numero di telefono utilizzato da un altro cliente")
        elif clients_collection.find_one({"mail":mail},{}):
            flash("Mail utilizzata da un altro cliente")
        else:
            clients_collection.insert_one(new_client)
            flash("Cliente aggiutno con successo")
            return redirect(url_for("views.clients"))
        
    form.nome.data = ""
    form.cognome.data = ""
    form.indirizzo.data = ""
    form.citta.data = ""
    form.cellulare.data = ""
    form.mail.data = ""
    form.azione.data = ""
    return render_template('insert_clients.html', form=form, nome=nome, cognome=cognome, indirizzo=azione, citta=citta, cellulare=cellulare, mail=mail, azione=azione)

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