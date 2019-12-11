from flask import Flask
from flask import render_template, redirect, url_for
from flask import request, session, flash
from .models import db
from .models import Kalkulacka, User
from datetime import datetime
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import IntegerField, SelectField, widgets, SubmitField, FileField, StringField, PasswordField
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename
import os

flask_app = Flask(__name__)
flask_app.config.from_pyfile("/vagrant/configs/default.py")
db.init_app(flask_app)

class Test(FlaskForm):
    cislo1 = IntegerField("Cislo 1", widget=widgets.Input(input_type="number"), validators=[InputRequired()])
    operator = SelectField("Operator", choices=[("+", "+"), ("-", "-"), ("/", "/"), ("*", "*")])
    cislo2 = IntegerField("Cislo 2", widget=widgets.Input(input_type="number"), validators=[InputRequired()])
    submit = SubmitField("Submit", render_kw=dict(class_= "btn btn-outline-primary btn-block"))

class Image(FlaskForm):
    image = FileField("image", validators=[FileRequired()])
    submit = SubmitField("Odeslat", render_kw=dict(class_= "btn btn-outline-primary btn-block"))

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


@flask_app.route("/")
def view_welcame_page():
    form = Test()
    return render_template("view_home.html", form=form)

@flask_app.route("/transaction/", methods=["GET"])
def completed_transactions():
    page = request.args.get("page", 1, type=int)
    paginate = Kalkulacka.query.order_by(Kalkulacka.id.desc()).paginate(page, 10, False)
    return render_template("transaction.html", trans=paginate.items, paginate=paginate)

@flask_app.route("/delete_trans/", methods=["GET"])
def delete_trans():
    if "user" not in session:
        return redirect(url_for("login"))
    tran_id = request.args.get("tran_id")
    page = request.args.get("page")
    tran = Kalkulacka.query.filter_by(id = tran_id).first()
    if tran:
        db.session.delete(tran)
        db.session.commit()
        flash("tran id: {} delete".format(tran_id), "alert-successful")
        return redirect(url_for("completed_transactions", page=page))
    return redirect(url_for("completed_transactions"))

@flask_app.route("/soucet/", methods=["GET", "POST"])
def soucet():
    form = Test()
    if form.validate_on_submit():
        cislo1 = form.cislo1.data
        cislo2 = form.cislo2.data
        operator = form.operator.data
        soucet = eval(str(cislo1) + operator + str(cislo2))
        num = Kalkulacka(num = soucet)
        db.session.add(num)
        db.session.commit()
        return render_template("soucet.html", soucet=soucet)
    return render_template("view_home.html", form=form)

@flask_app.route("/image/", methods=["GET", "POST"])
def add_image():
    form = Image()
    if form.validate_on_submit():
        file = form.image.data
        name = secure_filename(file.filename)
        file.save(os.path.join(flask_app.config["UPLOAD_FOLDER"], name))
    images = os.listdir(flask_app.config["UPLOAD_FOLDER"])
    return render_template("galerie.html", form=form, images=images)

@flask_app.route("/login/", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        if username == "admin" and password == "admin":
            session["user"] = username
            flash("login", "alert-successful")
            return redirect(url_for("view_welcame_page"))
        flash("bad data", "alert-fail")
    return render_template("login.html", form=login_form)

@flask_app.route("/logout/")
def logout():
    if "user" in session:
        session.pop("user")
        flash("logout")
        return redirect(url_for("login"))
    return render_template("view_welcame_page.html")

@flask_app.route("/register/", methods=["GET", "POST"])
def register():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print(user)
        if user:
            flash("Username is bug")
            return render_template("register.html", form=form)
        user = User(
            username = form.username.data,
            password = form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash("User create", "alert-successful")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@flask_app.context_processor
def inject_now():
    num = Kalkulacka.query.all()
    return {'now': datetime.utcnow(),
            'celkem': len(num)}


# <form action="{{ url_for('soucet') }}" method="get">
#       Cislo 1:<br>
#       <input type="number" name="cislo1">
#       <br>
#       Cislo 2:<br>
#       <input type="number" name="cislo2">
#       <br>
#       Znamenko:<br>
#       <input type="text" name="zna">
#       <br><br>
#       <input type="submit" value="Submit">
#     </form>