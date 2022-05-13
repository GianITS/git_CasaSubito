from crypt import methods
from logging import exception
from flask import Blueprint, flash, render_template, redirect, request, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from .models import agents_collection

auth = Blueprint('auth', __name__)

# crea form del login
class FormLogin(FlaskForm):
    utente = StringField("Utente", [DataRequired()], name="utente")
    password = PasswordField("Password", [DataRequired()])
    submit = SubmitField("Inserisci")

@auth.route('/', methods=["GET", "POST"])
def login():
    utente = ""
    password = ""
    form=FormLogin()
    if form.validate_on_submit():
        utente = form.utente.data
        password = form.password.data
        try:
            session["agent"] = agents_collection.find_one({"username":utente, "password":password},{"_id":0, "nome":1})['nome']
            form.utente.data = ""
            form.password.data = ""
            return redirect(url_for("views.home"))
        except:
            form.utente.data = ""
            form.password.data = ""
            flash("Utente non registrato")
        #     session["agent"] = None
        # if session["agent"] != None:
        #     form.utente.data = ""
        #     form.password.data = ""
        #     return redirect(url_for("views.home"))
        # else:
        #     form.utente.data = ""
        #     form.password.data = ""
        #     flash("Utente non registrato")
    
    return render_template('login.html',form=form, utente=utente, password=password)