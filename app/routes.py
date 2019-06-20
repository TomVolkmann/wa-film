from app import app, db
from app.forms import RegistrationForm
from flask import render_template, flash, redirect,url_for, request
from app.forms import LoginForm, PostMovieForm, PostNewsForm, ContactForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Movie, Post, Contact
from werkzeug.urls import url_parse
from werkzeug.exceptions import abort

###################### GENERAL NAV ###############################

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template("index.html", title='Home Page')

@app.route('/completed')
def completed(): 
    movies = Movie.query.filter_by(isReleased=1).all()
    return render_template('movies_completed.html', movies=movies)

@app.route('/development')
def development():
    movies = Movie.query.filter_by(isReleased=0).all()
    return render_template('movies_development.html',movies=movies)

@login_required
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    movies = Movie.query.all()
    posts = Post.query.all()
    contacts = Contact.query.all()
    return render_template('dashboard.html', movies = movies,posts=posts,contacts=contacts)

@app.route('/about')
def about(): 
    return render_template('about.html')

@app.route('/news')
def news():
    posts = Post.query.all()
    print(posts)
    return render_template('news.html', posts=posts)


###################### USER MANEGEMENT #########################
    
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

###################### MOVIES ####################################
@app.route('/movies/<movietitle>')
def movie(movietitle):
    movie = Movie.query.filter_by(title_DE=movietitle).first()
    return render_template('movie.html',movie=movie)

@app.route('/edit_movie', methods=['GET', 'POST'])
@login_required
def edit_movie():
    
    form = PostMovieForm()
    form.directors.choices = [(director.id, director.name) for director in Contact.query.all()]
     
    if form.validate_on_submit():
        #print(form.data['directors'][0])
        e = {
            'title_DE': form.data['title_DE'],
            'title_EN': form.data['title_EN'],
            'release_date': form.data['release_date'], 
            'isReleased': form.data['isReleased'],
            'directors': form.data['directors']
        }
        print(e)
        Movie.addMovie(e)
        flash('Your changes have been saved.')
        return redirect(url_for('edit_movie'))
    elif request.method == 'GET':
        id = request.args.get("id")
        if id is not None: 
            print(id)
            movie = Movie.getMovie(int(id))
            form.title_DE.data = movie.title_DE
            form.title_EN.data = movie.title_EN
       
    return render_template('edit.html', title='Edit Movie',form=form)

@app.route ('/delete_movie')
def delete_movie():
    id = int(request.args.get("id"))
    Movie.deleteMovie(id)
    return redirect(url_for('index'))

####################### POSTS ##############################

@app.route('/posts/<posttitle>')
def post(posttitle):
    post = Post.query.filter_by(title=posttitle).first()
    return render_template('post.html',post=post)

@app.route('/edit_post', methods=['GET', 'POST'])
@login_required
def edit_post():
    form = PostNewsForm()
    if form.validate_on_submit():
        e = {
            'user_id': current_user.id,
            'title': form.data['title'],
            'body': form.data['body'],
        }
        print(e)
        Post.addPost(e)
        flash('Your changes have been saved.')
        return redirect(url_for('edit_post'))
    elif request.method == 'GET':
        id = request.args.get("id")
        if id is not None: 
            print(id)
            post = Post.getPost(int(id))
            form.title.data = post.title
            form.body.data = post.body
       
    return render_template('edit_post.html', title="Edit Post", form=form)

@app.route ('/delete_post')
def delete_post():
    id = int(request.args.get("id"))
    Post.deletePost(id)
    return redirect(url_for('index'))


####################### CONTACTS ##############################

@app.route('/contacts/<contactid>')
def contact(contactid):
    contact = Contact.query.filter_by(id=contactid).first()
    return render_template('contact.html',contact=contact)

@app.route('/edit_contact', methods=['GET', 'POST'])
@login_required
def edit_contact():
    form = ContactForm()
    if form.validate_on_submit():
        e = {
            'name': form.data['name'],
        }
        print(e)
        Contact.addContact(e)
        flash('Your changes have been saved.')
        return redirect(url_for('edit_contact'))
    elif request.method == 'GET':
        id = request.args.get("id")
        if id is not None: 
            print(id)
            contact = Contact.getContact(int(id))
            form.name.data = contact.name
       
    return render_template('edit_contact.html', title="Edit Contact", form=form)

@app.route ('/delete_contact')
def delete_contact():
    id = int(request.args.get("id"))
    Contact.deleteContact(id)
    return redirect(url_for('index'))


####################### ABOUT    ##############################



