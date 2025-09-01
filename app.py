from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON, select
from datetime import timedelta
import json
from collections import defaultdict

app = Flask(__name__)
app.secret_key = 'sc2313ggdfg4454309hkfdjsfvbgdzamop'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days=5)

db = SQLAlchemy(app)


class Users(db.Model):
    __tablename__ = 'users'
    _id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column('Email', db.String(100))
    password = db.Column('Password', db.String(100))

    def __init__(self, email, password):
        self.email = email
        self.password = password


class Cars(db.Model):
    __tablename__ = 'cars'
    _id = db.Column('id', db.Integer, primary_key=True)
    car_type = db.Column(db.String(100))
    content = db.Column(JSON)

    def __init__(self, car_type, content):
        self.car_type = car_type
        self.content = content


class Images(db.Model):
    __tablename__ = 'images'
    _id = db.Column('id', db.Integer, primary_key=True)
    image_name = db.Column(db.String(100))
    image_file_path = db.Column(JSON)


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Users.query.filter_by(email=email).first()
        if user:
            flash('User already exists, try again')
            return redirect(url_for('signup'))
        new_user = Users(email=email, password=generate_password_hash(password, method='pbkdf2:sha256'))
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful, logging you in')
        return redirect(url_for('home'))
        
    return render_template('signup.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session.permanent = True
        email = request.form['email']
        password = request.form['password']
        user = Users.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['email'] = email
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))
    else:
        return render_template('login.html')

    
@app.route('/account', methods=['POST', 'GET'])
def account():
    if 'email' not in session:
        return redirect(url_for('login'))
    user = Users.query.filter_by(email=session['email']).first()
    if request.method == 'POST':
        new_email = request.form.get('email')
        new_password = request.form.get('password')
        if new_email:
            if Users.query.filter(Users.email == new_email).first():
                return redirect(url_for('account'))
            user.email = new_email
            session['email'] = new_email
            if new_password:
                user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
        return redirect(url_for('home'))
    return render_template('account.html')


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))


@app.context_processor
def images_to_page():
    all_images = Images.query.all()
    images = defaultdict(list)
    for img in all_images:
        images[img.image_name].extend(img.image_file_path)
    return dict(images=dict(images))


@app.context_processor
def context_processor():
    car_content = select(Cars.content)
    all_row = db.session.execute(car_content).mappings().all()
    car_vars = {}
    for i, row in enumerate(all_row, start=1):
        car_vars[f'vehicle{i}'] = row['content']
    return car_vars
    

@app.route('/')
def home():
    if 'email' in session:
        return render_template('index.html')
    return redirect(url_for('login'))


@app.route('/car_type')
def show_car_type():
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template('car_type.html')


@app.route('/car_type/<car_type>')
def car_conditional(car_type):
    if 'email' not in session:
        return redirect(url_for('login'))
    
    if car_type == 'hatchback':
        return render_template('car_hatch.html', car_type=car_type, images_to_page=images_to_page())
    elif car_type == 'suv':
        return render_template('car_suv.html', car_type=car_type)
    elif car_type == 'supercar':
        return render_template('car_super.html', car_type=car_type)
    elif car_type == 'electric':
        return render_template('car_electric.html', car_type=car_type)
    else:
        return redirect(url_for('show_car_type'))



if __name__ == '__main__':
    with app.app_context(): 
        db.create_all()
    app.run(debug=True)