from operator import pos
from types import TracebackType
from flask.helpers import flash
from flask_login import login_required, login_user, current_user
from flask_login.mixins import UserMixin
from flask_login.utils import logout_user
from werkzeug.wrappers import request
from wtforms.fields.simple import SubmitField
from voting import db
from voting.models import Position, User,Candidate
from voting.forms import AGSForm, GiantForm, PresidentForm, RegisterForm, LoginForm, CandidateForm, SecretaryForm, SportsDirectorForm, TreasurerForm, VicePresidentForm
from voting import app
from flask import render_template, url_for, redirect, request

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')
    

@app.route('/register',methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(name=form.username.data,email_address=form.email_address.data,department=form.department.data,password=form.password1.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('home_page'))
    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form = form)


@app.route('/login', methods=['GET','POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email_address = form.email_address.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('voting_page'))

        else:
            flash('Username and password are not match! Please try again', category='danger')
    return render_template('login.html', form = form)


@app.route('/voting', methods = ['POST',"GET"])
@login_required
def voting_page():
    all = GiantForm()
    
    if not current_user.has_user_voted(): 
        if all.validate_on_submit():
            c1 = Candidate.query.filter_by(name = all.president.example.data).first()
            c1.vote()
            c1 = Candidate.query.filter_by(name = all.vice_president.example.data).first()
            c1.vote()
            c1 = Candidate.query.filter_by(name = all.secretary.example.data).first()
            c1.vote()
            c1 = Candidate.query.filter_by(name = all.ags.example.data).first()
            c1.vote()
            c1 = Candidate.query.filter_by(name = all.treasurer.example.data).first()
            c1.vote()
            c1 = Candidate.query.filter_by(name = all.sports_director.example.data).first()
            c1.vote()
            current_user.vote_check()
            flash(f'You have successfully voted in this election. Thank you very much', category='success')
            return redirect(url_for('home_page'))
    else:
        logout_user()
        flash(f'You have already voted', category='danger')
        return redirect(url_for('home_page'))  
    
    return render_template('vote.html', all = all)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('home_page'))


@app.route('/addcandidate', methods=['POST','GET'])
@login_required
def add_candidate():
    form = CandidateForm()
    if current_user.is_user_admin():
        if form.validate_on_submit():
            candidate = Candidate(name = form.name.data, department = form.department.data, position = form.position.data)
            db.session.add(candidate)
            db.session.commit()
            flash(f'You have successfully added {candidate.name} as a candidate for this election',category='success')
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(f'There was an error with adding this candidate: {err_msg}', category='danger')
    else:
        return "You are not allowed to add candidates for this election"
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with adding this candidate: {err_msg}', category='danger')

    return render_template('add.html',form = form)

@app.route('/results')
def check_result():
    candidate = Candidate.query.order_by(Candidate.position).all()
    return render_template('check_result.html', candidate = candidate)
