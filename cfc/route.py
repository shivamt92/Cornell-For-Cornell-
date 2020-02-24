from flask import render_template, url_for, flash, redirect, request
from cfc import app
from cfc.forms import Signup,Login
from cfc.User import User, RefList
from cfc import bcrypt, db
from flask_login import login_user,current_user,logout_user, login_required

@app.route("/")
@app.route("/home")
def CFCProject():

    return render_template('home.html')

@app.route("/about")
def about():
    return "Shivam Tewari"


@app.route("/user_home")
@login_required
def user_home():
    return render_template('user_home.html')

@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('user_home'))
    form = Signup()
    if form.validate_on_submit():
        hash_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(netid = form.netid.data, first_name = form.first_name.data, last_name = form.last_name.data, email = form.cornell_email.data, password = hash_pass, major = form.major.data, type_id = form.type_field.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created for {} {}'.format(form.first_name.data,form.last_name.data), 'success')
        return redirect(url_for('CFCProject'))
    return render_template('signup.html', title = 'Signup', form = form)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user_home'))
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.cornell_email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('user_home') )

        else:
            flash('Login Unsuccessful check Email and Password', 'danger')
        # flash('Login Unsuccessful for {} {}'.format(form.first_name.data, form.last_name.data), 'success')
    return render_template('login.html', title = 'Login', form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('CFCProject'))