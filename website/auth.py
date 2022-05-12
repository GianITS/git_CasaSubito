from crypt import methods
from flask import Blueprint, render_template, redirect, request, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from .models import agents_collection, Agent

auth = Blueprint('auth', __name__)

# crea form del login
class FormLogin(FlaskForm):
    utente = StringField("Utente", [DataRequired()], name="utente")
    password = PasswordField("Password", [DataRequired()])
    submit = SubmitField("Inserisci")

@auth.route('/', methods=["GET", "POST"])
def login():
    utente = None
    password = None
    form=FormLogin()
    if form.validate_on_submit():
        utente = form.utente.data
        password = form.password.data
        session["agent"] = agents_collection.find_one({"username":utente, "password":password},{"_id":0, "nome":1})
        if session["agent"] != "" or session["agent"] != None:
            print(session["agent"]["nome"])
            return redirect(url_for("views.home"))
        form.utente.data = None
    return render_template('login.html',form=form, utente=utente, password=password)