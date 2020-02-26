from flask import render_template, url_for, flash, redirect, request
from cfc import app
from cfc.forms import Signup,Login, Ref_Post, SearchQuery
from cfc.User import User, RefList
from cfc import bcrypt, db
from flask_login import login_user,current_user,logout_user, login_required
from sqlalchemy import or_, and_

@app.route("/")
@app.route("/home")
def CFCProject():

    return render_template('home.html')

@app.route("/about")
def about():
    return "Shivam Tewari"


@app.route("/user_home", methods = ['GET'])
@login_required
def user_home():
    image = url_for('static', filename ='profile_pic'+current_user.image)
    return render_template('user_home.html', image = image)

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
        return redirect(url_for('login'))
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


@app.route("/post_ref", methods = ['GET', 'POST'])
def post_ref():
    if current_user.is_authenticated:

        form = Ref_Post()
        if form.validate_on_submit():
            ref = RefList(job_title = form.job_title.data, job_des = form.job_des.data, company = form.company.data, ref_id = current_user.id)
            db.session.add(ref)
            db.session.commit()
            flash('References posted for {} {}'.format(form.job_title.data, form.company.data), 'success')
            return redirect(url_for('user_home'))
        # else:
        #     flash('Incorrect information filled', 'danger')

        return render_template('post_reference.html', form = form)


@app.route("/references", methods = ['GET','POST'])
def references():
    if current_user.is_authenticated:
        form = SearchQuery()
        title = '%{}%'.format(form.job_title.data)
        comp = '%{}%'.format(form.company.data)
        query = db.session.query(RefList.job_title, RefList.company, RefList.ref_id).filter(and_(RefList.job_title.like(title),RefList.company.like(comp))).all()
        Ids = []
        for q in query:
            Ids.append(User.query.get(q[2]).email)

        return render_template('references.html', form = form, query = query, Ids = Ids)
