import os
from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
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

@app.route('/')
def index():
    # Consider displaying a welcome message or list of features here
    return render_template('rotaPrincipal.html')

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

@app.route('/professores')
def professores():
    return render_template('naoDisponivel.html')

@app.route('/alunos')
def naoDisponivel():
    return render_template('naoDisponivel.html')
    
@app.route('/cursos')
def cursos():
    return render_template('naoDisponivel.html')

@app.route('/ocorrencias')
def ocorrencias():
    return render_template('naoDisponivel.html')
