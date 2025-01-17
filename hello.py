import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from pytz import timezone

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define the disciplines table schema
class Discipline(db.Model):
    __tablename__ = 'disciplines'  # Ensure this matches the database table name

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)  # Adjust name length as needed
    semester = db.Column(db.String(20))  # Adjust semester field details as needed

# Create the disciplines table (if it doesn't exist)
with app.app_context():
    db.create_all()

# Create a form class for discipline data
class DisciplineForm(FlaskForm):
    name = StringField('Disciplina', validators=[DataRequired()])
    semester = StringField('Semestre', validators=[DataRequired()])
    submit = SubmitField('Cadastrar')


@app.route('/disciplinas', methods=['GET', 'POST'])
def disciplinas():
    form = DisciplineForm()
    if form.validate_on_submit():
        # Process form data
        new_discipline = Discipline(name=form.name.data, semester=form.semester.data)
        db.session.add(new_discipline)
        db.session.commit()
        flash('Disciplina cadastrada com sucesso!')
        return redirect(url_for('disciplinas'))  # Redirect to prevent form resubmission

    # Get all disciplines from the database (assuming you have a query method)
    disciplines = Discipline.query.all()

    return render_template('cadastroDeDisciplina.html', form=form, disciplines=disciplines)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/indisponivel', methods=['GET', 'POST'])
def indisponivel():
     return render_template('indisponivel.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    brasil_tz = timezone('America/Sao_Paulo')
    now = datetime.now(brasil_tz)
    current_time = now.strftime("%Y-%M-%d %H:%M:%S")
    return render_template('home.html', current_time=current_time)







    
