from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_wtf import FlaskForm
from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Users
from flask_mail import Message
from extensions import db, mail, csrf

main_bp = Blueprint('main', __name__)


class ResetRequestForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired()])
    submit = SubmitField(label='Reset Password')

class ResetPasswordForm(FlaskForm):
    password = PasswordField(label='Password', validators=[DataRequired()])
    confirm_password = PasswordField(label='Confirm Password', validators=[DataRequired()])
    submit = SubmitField(label='Change Password')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class AccountForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Update Account Details')

class SignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Signup')


@main_bp.route('/signup', methods=['POST', 'GET'])
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')

        user = Users.query.filter_by(email=email).first()
        if user:
            flash('User already exists, try again')
            return redirect(url_for('main.signup'))
        new_user = Users(email=email, password=generate_password_hash(password, method='pbkdf2:sha256'))
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful, logging you in')
        return redirect(url_for('main.home'))
        
    return render_template('signup.html', form=form)


@main_bp.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        session.permanent = True
        email = request.form['email']
        password = request.form['password']
        user = Users.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['email'] = email
            flash('Login successful!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid email or password', 'error')
            return redirect(url_for('main.login'))
    return render_template('login.html', form=form)

    
@main_bp.route('/account', methods=['POST', 'GET'])
def account():
    if 'email' not in session:
        return redirect(url_for('main.login'))
    form = AccountForm()
    user = Users.query.filter_by(email=session['email']).first()
    if request.method == 'POST' and form.validate_on_submit():
        new_email = request.form.get('email')
        new_password = request.form.get('password')
        if new_email:
            if Users.query.filter(Users.email == new_email).first():
                return redirect(url_for('account'))
            user.email = new_email
            session['email'] = new_email
            if new_password:
                user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
        return redirect(url_for('main.home'))
    return render_template('account.html', form=form)

def send_mail(user):
    token = user.get_token()
    msg = Message('Password Reset Request', recipients=[user.email], sender='noreply@quicheandbeans.com')
    msg.body = f''' To reset your password, please click the link below.
    
    {url_for('reset_token', token=token, _external=True)}

    If you did not send a password reset request, please ignore this message.

    '''
    mail.send(msg)

@main_bp.route('/reset_password', methods=['POST', 'GET'])
def reset_password():
    form = ResetRequestForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            send_mail(user)
        flash('A reset link has been sent to your email.', 'success')
        return redirect(url_for('main.login'))
    return render_template('reset_password.html', form=form)


@main_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    user = Users.verify_token(token)
    if user is None:
        flash('That is an invalid token or token has expired.', 'warning')
        return redirect(url_for('main.reset_password'))
    
    form = ResetPasswordForm()
    form.token = token
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        user.password = hashed_password
        db.session.commit()
        flash('Password changed!', 'success')
        return redirect(url_for('main.login'))
    return render_template('change_password.html', form=form, token=token)
    

@main_bp.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('main.login'))


@main_bp.route('/search_result')
def search_result():
    if 'email' not in session:
        return redirect(url_for('main.login'))
    return render_template('search_result.html')
    

@main_bp.route('/')
def home():
    if 'email' not in session:
        return redirect(url_for('main.login'))
    return render_template('index.html')
    


@main_bp.route('/car_type')
def show_car_type():
    if 'email' not in session:
        return redirect(url_for('main.login'))
    return render_template('car_type.html')


@main_bp.route('/car_type/<car_type>')
def car_conditional(car_type):
    if 'email' not in session:
        return redirect(url_for('main.login'))
    
    if car_type == 'hatchback':
        return render_template('car_hatch.html', car_type=car_type)
    elif car_type == 'suv':
        return render_template('car_suv.html', car_type=car_type)
    elif car_type == 'supercar':
        return render_template('car_super.html', car_type=car_type)
    elif car_type == 'electric':
        return render_template('car_electric.html', car_type=car_type)
    else:
        return redirect(url_for('main.show_car_type'))

