from flask import Blueprint,render_template,redirect,url_for

views = Blueprint("views", __name__)

@views.route("/")
def start():
    return render_template("login.html")

@views.route("/home")
def home():
    return render_template("home.html")

@views.route("/immobili")
def imm():
    return render_template("immobili.html")

@views.route("/client")
def client():
    return render_template("client.html")
    
@views.route("/user")
def user():
    return render_template("user.html")

@views.route("/add_immobile")
def popup_immobile():
    return render_template("add_imm.html")