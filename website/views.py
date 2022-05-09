from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/HomePage')
def home():
    return render_template('homepage.html')