from ast import Num
from flask import Blueprint, render_template, request,session, redirect,url_for,flash
from .models import cltImmobili

auth = Blueprint("auth", __name__)

@auth.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        password = request.form["psw"]
        return redirect(url_for("views.home"))

@auth.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("views.start"))

@auth.route("/add_immobile", methods=["POST", "GET"])
def new_immobile():
    if request.method == "POST":
        address = request.form.get('address')
        city = request.form.get('city')
        proprietario = request.form.get('proprietario')
        m2:Num = request.form.get('m^2')

        """ 
        if address:
            flash('address already exists.', category='error')
        el
        """
        
        
        if len(address) == 0:
            flash('enter address.', category='error')
        elif len(city) == 0:
            flash('enter city.', category='error')
        elif len(proprietario) == 0:
            flash('enter proprietario.', category='error')
        elif len(m2) == 0:
            flash('enter grandezza.', category='error')
        else: 
            new_immobile = {"address": address, "proprietario":proprietario, "city":city, "m^2":m2}
            cltImmobili.insert_one(new_immobile)
            flash('immobile inserito!', category='success')

            #login_user(new_user, remember=True)
            #flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return redirect(url_for('views.popup_immobile'))


