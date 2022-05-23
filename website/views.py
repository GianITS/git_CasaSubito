from crypt import methods
import datetime
from flask import Blueprint, Flask, render_template, request, session, redirect, url_for, flash
from flask_pymongo import PyMongo
import certifi

views = Blueprint('views', __name__)

# PyMongo ---------------------------------------------------------------------
app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb+srv://GianITS:ProjectITS33@clusterits.do6lt.mongodb.net/Agenzia_Immo?retryWrites=true&w=majority"
#app.config['MONGO_URI'] = "mongodb://admin:Passw0rd!@192.168.43.75/DB_prova?retryWrites=true&w=majority"
mongo = PyMongo(app, tlsCAFile=certifi.where())


@views.route('/HomePage')
def home():
    date = datetime.datetime.now()
    date=date.strftime("%A %d %B %Y")
    return render_template('homepage.html', date=date)

@views.context_processor
def base():
    form = FormSearch()
    return dict(form=form)

# importo i moduli relativi al form
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, RadioField, MultipleFileField, SelectField, TextAreaField, EmailField
from wtforms.validators import DataRequired, InputRequired
from .models import properties_collection, clients_collection

class FormSearch(FlaskForm):
    testo = StringField("", [DataRequired()])
    submit = SubmitField("")

@views.route('/HomePage', methods=['GET','POST'])
def search():
    testo = ""
    form = FormSearch()
    if form.validate_on_submit():
        testo = form.testo.data
        print(testo)
        resCN = list(clients_collection.find({"nome": testo}, {"nome":1,"_id":0}))
        resCC = list(clients_collection.find({"cognome": testo}, {"nome":1,"_id":0}))
        resI = list(properties_collection.find({"indirizzo": testo}, {"nome":1,"_id":0}))
        if resCN or resCC:
            res = resCN[0]['nome']
            print(res)
            return redirect(url_for("views.ClientPage", nome=res))
        elif resI:
            res = resI[0]['nome']
            print(res)
            return redirect(url_for("views.PropPage", nome=res))
        else:
            print("non trovato")
            flash("Nessun risultato trovato")
        print(f"resCN = {resCN}\nresCC = {resCC}\nresI = {resI}")

    form.testo.data = ""
    return render_template("homepage.html", form=form)

#funzione rimuovi document dal db

@views.route('/Clienti/<nome>', methods=['GET','POST'])
def removeC(nome):
    query = clients_collection.find_one_and_delete({"nome":nome})
    if query:
        flash("Cliente rimosso con successo", 'success')
    else:
        flash("Cliente non trovato", 'error')
    return redirect(url_for('views.clients'))

@views.route('/Immobili/<nome>', methods=['GET','POST'])
def removeP(nome):
    query = properties_collection.find_one_and_delete({"nome":nome})
    if query:
        flash("Immobile rimosso con successo", 'success')
    else:
        flash("Immobile non trovato", 'error')
    return redirect(url_for('views.properties'))

# pagina inserimento cliente

class FormInsertClient(FlaskForm):
    nome = StringField("Nome:", [DataRequired()])
    cognome = StringField("Cognome:", [DataRequired()])
    indirizzo = StringField("Indirizzo:", [DataRequired()])
    citta = StringField("citta:", [DataRequired()])
    cellulare = IntegerField("Cellulare:", [DataRequired()])
    mail = EmailField("Email:", [DataRequired()])
    azione = RadioField("Compra/Vende:", validators=[InputRequired()], choices = [("Compra", "Compra"), ("Vende", "Vende")])
    agent = StringField("Agente:")
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
    agent = session['agent']

    form=FormInsertClient()
    if form.validate_on_submit():
        nome = form.nome.data
        cognome = form.cognome.data
        indirizzo = form.indirizzo.data
        citta = form.citta.data
        cellulare = form.cellulare.data
        mail = form.mail.data
        azione = form.azione.data

        new_client = {"nome":nome, "cognome":cognome, "indirizzo":indirizzo, "citta":citta, "cell":cellulare, "mail":mail, "buysellrent":azione, "agente":agent}

        if clients_collection.find_one({"cellulare":cellulare},{}):
            flash("Numero di telefono utilizzato da un altro cliente")
        elif clients_collection.find_one({"mail":mail},{}):
            flash("Mail utilizzata da un altro cliente")
        else:
            clients_collection.insert_one(new_client)
            flash("Cliente aggiunto con successo")
            return redirect(url_for("views.clients"))
        
    form.nome.data = ""
    form.cognome.data = ""
    form.indirizzo.data = ""
    form.citta.data = ""
    form.cellulare.data = 0
    form.mail.data = ""
    form.azione.data = ""
    return render_template('insert_clients.html', form=form, nome=nome, cognome=cognome, indirizzo=azione, citta=citta, cellulare=cellulare, mail=mail, azione=azione, agent=agent)

# pagina clienti totali

listHeadClient = ["Nome", "Cognome", "Telefono", "E-mail", "Compra\nAffitta", "Agente"]
@views.route('/Clienti')
def clients():
    clienti = list(clients_collection.find({},{"_id":0}))[::-1]
    return render_template('clients.html', clienti=clienti, listHeadClient=listHeadClient)
    
# pagina singolo cliente

@views.route('/PaginaCliente/<nome>')
def ClientPage(nome):
    client = clients_collection.find_one({"nome": nome}, {"_id":0})
    client =list(client.values())
    cognome = client[1]
    indirizzo = client[2]
    citta = client[3]
    cellulare = client[4]
    mail = client[5]
    azione = client[6]
    if client.__len__() == 9: 
        immobile = list(client[8].values())
        indirizzo2 = immobile[0]
        citta2 = immobile[1]
        vendAff = immobile[3]
        mQuadri = immobile[4]
        totStanze = immobile[5]
        string = ""
    else:
        string = "Nessun immobile collegato"
        indirizzo2 = ""
        citta2 = ""
        vendAff = ""
        mQuadri = ""
        totStanze = ""
    return render_template('clients_page.html', nome=nome, cognome=cognome, indirizzo=indirizzo, citta=citta, cellulare=cellulare, mail=mail, azione=azione, indirizzo2=indirizzo2, citta2=citta2, vendAff=vendAff, mQuadri=mQuadri, numStanze=totStanze, string=string)

# pagina immobili totali

listHead = ["Nome", "Cognome", "Indirizzo", "Citta", "Tipologia", "Vendita\nAffitto", "Metri\nquadri", "Agente"]
@views.route('/Immobili')
def properties():
    immobili = list(properties_collection.find({},{"_id":0}))[::-1]
    return render_template('properties.html', immobili=immobili, listHead=listHead)

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

#creo la classe form dell inserimento degli immobili

#  inserire tipologia immobile:
# (appartamento/casa indipendente/casa semindipendente/villa a schiera/rustico)
class FormInsertProperties(FlaskForm):
    owner = StringField("Proprietario:")
    ownerName = StringField("Nome:", validators=[DataRequired()])
    ownerLastname = StringField("Cognome:", validators=[DataRequired()])
    address = StringField("Indirizzo:", validators=[DataRequired()])
    city = StringField("Citta:", validators=[DataRequired()])
    tipologia = SelectField(u"Tipologia:", choices=[('Appartamento', 'Appartamento'),('Casa indipendente','Casa indipendente'),('Casa semindipendente','Casa semindipendente'),('Villa a schiera','Villa a schiera'),('Rustico','Rustico')])
    vendAff = RadioField("Vendita/Affitto:", validators=[InputRequired()], choices=[('Vendita','Vendita'),('Affitto','Affitto')])
    sqMeters = IntegerField("Dimensioni:", validators=[DataRequired()])
    totRoom = IntegerField("Totale stanze:", validators=[DataRequired()])
    description = TextAreaField("Descrizione:", validators=[DataRequired()])
    images = MultipleFileField("Carica immagini:")
    agent = StringField("Agente:")
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
        post1 = {"indirizzo":address, "citta":city, "tipologia":tipologia, "vendAff":vendAff, "dimensioni":sqMeters, "totroom": totRoom, "textbox":description, "immagini": listImg, "agente":agent}
        clients_collection.update_one({"nome":ownerName, "cognome":ownerLastname},{"$set":{"immobili":post1}})
        post2 = {"nome":ownerName, "cognome":ownerLastname, "indirizzo":address, "citta":city, "typehouse":tipologia, "sellrent":vendAff, "dimensioni":sqMeters, "totroom": totRoom, "textbox":description, "immagini": listImg, "agente":agent}
        properties_collection.insert_one(post2)
        flash("Immobile inserito con successo")
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
    prop = list(prop.values())
    cognome=prop[0]
    indirizzo=prop[1]
    citta=prop[2]
    tipologia=prop[3]
    vendAff=prop[4]
    mQuadri=prop[5]
    numStanze=prop[6]
    descrizione=prop[7]
    client = clients_collection.find_one({"nome": nome}, {"indirizzo":1, "citta":1, "cell":1, "mail":1, "_id":0})
    client = list(client.values())
    indirizzo2 = client[0]
    citta2 = client[1]
    cellulare = client[2]
    mail = client[3]
    return render_template('property_page.html', nome=nome, cognome=cognome, indirizzo=indirizzo, citta=citta, tipologia=tipologia, mQuadri=mQuadri, numStanze=numStanze, vendAff=vendAff, descrizione=descrizione, indirizzo2=indirizzo2, citta2=citta2, cellulare=cellulare, mail=mail)

# pagina immagini immobile

@views.route('/PaginaImmobile/<nome>/Immagini')
def showImg(nome):
    img = properties_collection.find_one({"nome": nome}, {"immagini":1, "_id":0})
    for k,v in img.items():
        listImg = v
    return render_template('show_img.html', nome=nome, listImg=listImg)


if __name__ == "__main__":
    query = clients_collection.find({})
    for x in query:
        print(x)