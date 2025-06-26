from functools import wraps
from flask import Flask, render_template, redirect, request, session, url_for, g
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('PLANNER_SECRET_KEY', 'change-me')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='open')


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    date = db.Column(db.String(50))
    description = db.Column(db.Text)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    quantity = db.Column(db.Integer)
    description = db.Column(db.Text)


@app.before_first_request
def create_tables():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        password = os.environ.get('PLANNER_ADMIN_PASSWORD', 'admin')
        hashed = generate_password_hash(password)
        user = User(username='admin', password_hash=hashed)
        db.session.add(user)
        db.session.commit()


@app.before_request
def load_user():
    g.user = None
    if logged_in():
        g.user = User.query.get(session['user_id'])


def logged_in() -> bool:
    return 'user_id' in session


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not logged_in():
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrapper


@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            return redirect(url_for('index'))
        return render_template('login.html', error='Ungültige Zugangsdaten')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error='Benutzer existiert bereits')
        hashed = generate_password_hash(password)
        user = User(username=username, password_hash=hashed)
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        return redirect(url_for('index'))
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/tickets')
@login_required
def tickets():
    tickets = Ticket.query.all()
    return render_template('tickets.html', tickets=tickets)


@app.route('/calendar')
@login_required
def calendar_view():
    events = Event.query.all()
    return render_template('calendar.html', events=events)


@app.route('/inventory')
@login_required
def inventory():
    items = Item.query.all()
    return render_template('inventory.html', items=items)


if __name__ == '__main__':
    app.run(debug=True)
