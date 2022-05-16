from flask import Blueprint, Flask, render_template, request, session, redirect, url_for, flash
from flask_pymongo import PyMongo
import certifi

views = Blueprint('views', __name__)

# PyMongo ---------------------------------------------------------------------
app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb+srv://GianITS:ProjectITS33@clusterits.do6lt.mongodb.net/Agenzia_Immo?retryWrites=true&w=majority"
mongo = PyMongo(app, tlsCAFile=certifi.where())


@views.route('/HomePage')
def home():
    return render_template('homepage.html')

# import
from .models import clients_collection

@views.route('/Clienti')
def clients():
    clienti = list(clients_collection.find({},{"_id":0}))
    return render_template('clients.html', clienti=clienti)

@views.route('/Inserimento_Clienti')
def insert_clients():
    return render_template('insert_clients.html')

# import
from .models import properties_collection

@views.route('/Immobili')
def properties():
    immobili = list(properties_collection.find({},{"_id":0}))
    return render_template('properties.html', immobili=immobili)

# import
import gridfs
from urllib import response
from .models import db
# recupero le immagini dal db
@views.route('/image/<filename>')
def image(filename):
    fs = gridfs.GridFS(db)
    gridout = fs.get_last_version(filename=filename)
    response.content_type = 'image/jpeg'
    return gridout.read()

# importo i moduli relativi al form
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, RadioField, MultipleFileField, SelectField
from wtforms.validators import DataRequired

#creo la classe form dell inserimento degli immobili
class FormInsertProperties(FlaskForm):
    owner = StringField("Proprietario", validators=[DataRequired()])
    sqMeters = IntegerField("Dimensioni", validators=[DataRequired()])
    address = StringField("Posizione", validators=[DataRequired()])
    city = StringField("Posizione", validators=[DataRequired()])
    vendAff = RadioField("Vendita/Affitto", validators=[DataRequired()], choices=[('Vendita','Vendita'),('Affitto','Affitto')], default="Vendita")
    specifichePrinc = SelectField(u"Specifiche Principali", choices=[('Soggiorno con angolo cottura', 'Soggiorno con angolo cottura'),('Cucina','Cucina'),('Soggiorno','Soggiorno'),('Sala da pranzo','Sala da pranzo'),('Sala da pranzo','Sala da pranzo')])
    images = MultipleFileField("Carica immagini", validators=[DataRequired()])
    agent = StringField("agent")
    submit = SubmitField("Inserisci")

@views.route('/Inserimento_Immobili', methods=["GET", "POST"])
def insert_properties():
    # resetto tutte le variabili
    # assegno la variabile agente col nome dell agente loggato
    # assegno alla variabile form il form che ho appena creato
    owner = ""
    sqMeters = ""
    position = ""
    vendAff = ""
    images = ""
    agent = session['agent']
    form = FormInsertProperties()

    if form.validate_on_submit():
        owner = form.owner.data
        sqMeters = form.sqMeters.data
        position = form.position.data
        vendAff = form.vendAff.data
        images = request.files.getlist('images')
        listImg = []
        for image in images:
            #mongo.save_file(image.filename, image)
            listImg.append(image.filename)
        for img in listImg:
            print(img)
    
    #resetto i dati ricevutid dal form
    form.owner.data = ""
    form.sqMeters.data = ""
    form.position.data = ""
    form.vendAff.data = ""

    return render_template('insert_properties.html', form=form, owner=owner, sqMeters=sqMeters, position=position, vandAff=vendAff, images=images, agent=agent)

# pagina scheda immobile

from .models import properties_collection
@views.route('/PaginaImmobile/<nome>')
def PropPage(nome):
    prop = properties_collection.find_one({"nome": nome}, {"immagini":0, "_id":0})
    prop =list(prop.values())
    indirizzo=prop[1]
    citta=prop[2]
    mQuadri=prop[3]
    numStanze=prop[4]
    vendAff=prop[5]
    return render_template('property_page.html', nome=nome, indirizzo=indirizzo, citta=citta, mQuadri=mQuadri, numStanze=numStanze, vendAff=vendAff)

# pagina immagini immobile

@views.route('/PaginaImmobile/<nome>/Immagini')
def showImg(nome):
    img = properties_collection.find_one({"nome": nome}, {"immagini":1, "_id":0})
    for k,v in img.items():
        listImg = v
    return render_template('show_img.html', nome=nome, listImg=listImg)

@views.route('/RichiesteImmobiliari')
def properties_request():
    return render_template('properties_request.html')

if __name__ == "__main__":
    query = clients_collection.find({})
    for x in query:
        print(x)