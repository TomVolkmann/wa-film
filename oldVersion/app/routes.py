from app import app
from app import render_template, request, redirect, flash
from app.forms import LoginForm, PostMovieForm, RegistrationForm
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user
from database import User

import main
import database

@app.route('/index')
def index(): 
    form = PostMovieForm() 
    entries = database.get_movies()
    return render_template('show_entries.html', form=form,entries=entries)

@app.route ('/add_entry', methods=['POST'])
def add_entry():
    form = PostMovieForm() 

    if form.validate():
        e = {
            'title': form.data['title'],
            'release_date': form.data['release_date'],
            'contact': form.data['contact']
        }
        print(e)
        database.saveNewMovie(e)
    return redirect('/index')

@app.route ('/delete')
def delete_movie():
    id = int(request.args.get("id"))

    database.deleteMovies(id)

    return redirect("/index")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        database.session.add(user)
        database.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# @app.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('show_entries'))

