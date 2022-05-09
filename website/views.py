from flask import Blueprint, render_template

views = Blueprint('views', __name__)

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