from app import app, db
from app.forms import RegistrationForm
from flask import render_template, flash, redirect,url_for, request
from app.forms import LoginForm, PostMovieForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Movie
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template("index.html", title='Home Page')

@app.route('/show')
def show_entries(): 
    form = PostMovieForm() 
    entries = Movie.getMovies()
    return render_template('show_entries.html', form=form,entries=entries)

@app.route ('/add_entry', methods=['POST'])
def add_movie():
    form = PostMovieForm() 
    e = {
        'title_DE': form.data['title_DE'],
        'title_EN': form.data['title_EN'],
        'release_date': form.data['release_date'], 
        'isReleased': form.data['isReleased']
    }
    print(e)
    Movie.addMovie(e)
    return redirect(url_for('show_entries'))

@app.route ('/delete')
def delete_movie():
    id = int(request.args.get("id"))

    Movie.deleteMovie(id)

    return redirect(url_for('index'))

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
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))