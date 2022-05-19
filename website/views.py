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

# pagina inserimento cliente
# import
from .models import clients_collection

@views.route('/Inserimento_Clienti')
def insert_clients():
    return render_template('insert_clients.html')

# pagina clienti totali

@views.route('/Clienti')
def clients():
    clienti = list(clients_collection.find({},{"_id":0}))
    return render_template('clients.html', clienti=clienti)

# pagina singolo cliente

@views.route('/PaginaCliente/<nome>')
def ClientPage(nome):
    client = clients_collection.find_one({"nome": nome}, {"_id":0})
    client =list(client.values())
    cognome=client[1]
    indirizzo=client[2]
    citta=client[3]
    cellulare=client[4]
    mail=client[5]
    azione=client[6]
    return render_template('clients_page.html', nome=nome, cognome=cognome, indirizzo=indirizzo, citta=citta, cellulare=cellulare, mail=mail, azione=azione)

# pagina immobili totali
# import
from .models import properties_collection

@views.route('/Immobili')
def properties():
    immobili = list(properties_collection.find({},{"_id":0}))
    return render_template('properties.html', immobili=immobili)

# recupero le immagini dal db
# import
import gridfs
from urllib import response
from .models import db

@views.route('/image/<filename>')
def image(filename):
    fs = gridfs.GridFS(db)
    gridout = fs.get_last_version(filename=filename)
    response.content_type = 'image/jpeg'
    return gridout.read()

# importo i moduli relativi al form
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, RadioField, MultipleFileField, SelectField, TextAreaField
from wtforms.validators import DataRequired

#creo la classe form dell inserimento degli immobili


#  inserire tipologia immobile:
# (appartamento/casa indipendente/casa semindipendente/villa a schiera/rustico)
class FormInsertProperties(FlaskForm):
    owner = StringField("Proprietario: ")
    ownerName = StringField("Nome: ")
    ownerLastname = StringField("Cognome: ")
    address = StringField("Indirizzo: ")
    city = StringField("Citta: ")
    tipologia = SelectField(u"Tipologia: ", choices=[('Appartamento', 'Appartamento'),('Casa indipendente','Casa indipendente'),('Casa semindipendente','Casa semindipendente'),('Villa a schiera','Villa a schiera'),('Rustico','Rustico')])
    vendAff = RadioField("Vendita/Affitto: ", choices=[('Vendita','Vendita'),('Affitto','Affitto')], default="Vendita")
    sqMeters = IntegerField("Dimensioni: ")
    totRoom = IntegerField("Totale stanze: ")
    description = TextAreaField("Descrizione: ")
    images = MultipleFileField("Carica immagini: ")
    agent = StringField("Agente: ")
    submit = SubmitField("Inserisci")

@views.route('/Inserimento_Immobili', methods=["GET","POST"])
def insert_properties():
    # resetto tutte le variabili
    # assegno la variabile agente col nome dell agente loggato
    # assegno alla variabile form il form che ho appena creato
    ownerName = ""
    ownerLastname = ""
    address = ""
    city = ""
    tipologia = ""
    vendAff = ""
    sqMeters = ""
    totRoom = ""
    description = ""
    images = ""
    agent = session['agent']
    form = FormInsertProperties()

    if form.validate_on_submit():
        ownerName = form.ownerName.data
        ownerLastname = form.ownerLastname.data
        address = form.address.data
        city = form.city.data
        tipologia = form.tipologia.data
        vendAff = form.vendAff.data
        sqMeters = form.sqMeters.data
        totRoom = form.totRoom.data
        description = form.description.data
        images = request.files.getlist('images')
        listImg = []
        for image in images:
            mongo.save_file(image.filename, image)
            listImg.append(image.filename)
        post = {"nome":ownerName, "cognome":ownerLastname, "indirizzo":address, "citta":city, "tipologia":tipologia, "vendAff":vendAff, "dimensioni":sqMeters, "totStanze": totRoom, "descrizione":description, "immagini": listImg, "agente":agent}
        properties_collection.insert_one(post)
        return redirect(url_for('views.PropPage', nome=ownerName))
        
    
    #resetto i dati ricevutid dal form
    form.ownerName.data = ""
    form.ownerLastname.data = ""
    form.address.data = ""
    form.city.data = ""
    form.tipologia.data = ""
    form.vendAff.data = ""
    form.sqMeters.data = 0
    form.totRoom.data = 0
    form.description.data = ""
    form.images.data = ""

    return render_template('insert_properties.html', form=form, ownerName=ownerName, ownerLastname=ownerLastname, tipologia=tipologia, address=address, city=city, vandAff=vendAff, sqMeters=sqMeters, totRoom=totRoom, description=description, images=images, agent=agent)

# pagina scheda immobile

from .models import properties_collection
@views.route('/PaginaImmobile/<nome>')
def PropPage(nome):
    prop = properties_collection.find_one({"nome": nome}, {"nome":0, "immagini":0, "_id":0})
    prop =list(prop.values())
    cognome=prop[0]
    indirizzo=prop[1]
    citta=prop[2]
    tipologia=prop[3]
    vendAff=prop[4]
    mQuadri=prop[5]
    numStanze=prop[6]
    descrizione=prop[7]
    return render_template('property_page.html', nome=nome, cognome=cognome, indirizzo=indirizzo, citta=citta, tipologia=tipologia, mQuadri=mQuadri, numStanze=numStanze, vendAff=vendAff, descrizione=descrizione)

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