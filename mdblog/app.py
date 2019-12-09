from flask import Flask
from flask import render_template
from flask import request
from .models import db
from .models import Kalkulacka
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, widgets, SubmitField
from wtforms.validators import InputRequired

flask_app = Flask(__name__)
flask_app.config.from_pyfile("/vagrant/configs/default.py")

db.init_app(flask_app)

class Test(FlaskForm):
    cislo1 = IntegerField("Cislo 1", widget=widgets.Input(input_type="number"), validators=[InputRequired()])
    operator = SelectField("Operator", choices=[("+", "+"), ("-", "-"), ("/", "/"), ("*", "*")])
    cislo2 = IntegerField("Cislo 2", widget=widgets.Input(input_type="number"), validators=[InputRequired()])
    submit = SubmitField("Submit", render_kw=dict(class_= "btn btn-outline-primary btn-block"))


@flask_app.route("/")
def view_welcame_page():
    form = Test()
    return render_template("view_home.html", form=form)

@flask_app.route("/transaction/", methods=["GET"])
def completed_transactions():
    page = request.args.get("page", 1, type=int)
    paginate = Kalkulacka.query.order_by(Kalkulacka.id.desc()).paginate(page, 10, False)
    return render_template("transaction.html", trans=paginate.items, paginate=paginate)

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