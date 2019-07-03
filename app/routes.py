from app import app, db
from app.forms import RegistrationForm
from flask import render_template, flash, redirect,url_for, request, send_from_directory
from app.forms import LoginForm, PostMovieForm, PostNewsForm,  ContactForm, UploadForm, AboutContactForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Movie, Post, Contact, DesignImage
from werkzeug.urls import url_parse
from werkzeug.exceptions import abort

from werkzeug.utils import secure_filename
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField
import os
import hashlib
import time

###################### GENERAL NAV ###############################

@app.route('/')
@app.route('/index')
def index():
    designImage = DesignImage.query.filter_by(section="home", current=1).first()
    return render_template("index.html", title='Home Page', designImage=designImage)

@app.route('/completed')
def completed(): 
    movies = Movie.query.filter_by(isReleased=1).all()
    designImage = DesignImage.query.filter_by(section="completed_movies", current=1).first()
    return render_template('movies_completed.html', movies=movies, designImage=designImage)

@app.route('/development')
def development():
    movies = Movie.query.filter_by(isReleased=0).all()
    designImage = DesignImage.query.filter_by(section="movies_in_development", current=1).first()
    return render_template('movies_development.html',movies=movies, designImage=designImage)

@login_required
@app.route('/dashboard', methods=['GET', 'POST'])
@app.route ('/dashboard_movies')
def dashboard():
    movies = Movie.query.all()
    return render_template('dashboard_movies.html', movies = movies)

#src: Answer from Fahad Haleem https://stackoverflow.com/questions/7165749/open-file-in-a-relative-location-in-python 
# def readFile(filename):
#     filehandle = open(filename)
#     print (filehandle.read())
#     filehandle.close()

@app.route('/about')
def about(): 
    about_users = User.get_about()
    general = User.get_general()
    designImage = DesignImage.query.filter_by(section="about", current=1).first()

    #hardcoded path!
    with open('app\static\\about\About.txt', 'r') as file:
        data = file.read()
        #print(data)

    # return render_template('about.html', designImage=designImage, data=data)
    return render_template('about.html', designImage=designImage, about_users=about_users, general=general, data=data)


@app.route('/news')
def news():
    posts = Post.query.all()
    designImage = DesignImage.query.filter_by(section="news", current=1).first()
    #print(designImage.image_url)
    #print(posts)
    return render_template('news.html', posts=posts, designImage=designImage)


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
@login_required
def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
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
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/movies/<movietitle>')
def movie(movietitle):
    #Get Movie id
    movie_result = Movie.query.filter_by(title_DE = movietitle).first()

    directors = Contact.getContacts(movie_result.directors)
    producers = Contact.getContacts(movie_result.producers)
    executive_producers = Contact.getContacts(movie_result.executive_producers)
    editors = Contact.getContacts(movie_result.editors)
    cinematography = Contact.getContacts(movie_result.cinematography)
    sound_recordist = Contact.getContacts(movie_result.sound_recordist)
    sound_mix = Contact.getContacts(movie_result.sound_mix)
    color = Contact.getContacts(movie_result.color)

    if movie_result.release_date:
        release_date = movie_result.release_date
    else: 
        release_date = []

    if movie_result.isReleased:
        isReleased = movie_result.isReleased
    else:
        isReleased = []
    
    if movie_result.duration:
        duration = movie_result.duration
    else:
        duration = []

    if movie_result.synopsis:
        synopsis = movie_result.synopsis
    else:
        synopsis = []

    isColored = ""
    if movie_result.isColored == "b_w": 
        isColored = "Black & White" 
    else: 
        isColored = "Color"

    if movie_result.format: 
        format = movie_result.format.split(";")
    else: 
        format = []

    if movie_result.language: 
        language = movie_result.language.split(";") 
    else: 
        language = []

    if movie_result.awards: 
        awards = movie_result.awards.split(";") 
    else: 
        awards = []

    if movie_result.screenings: 
        screenings = movie_result.screenings.split(";") 
    else: 
        screenings = []

    if movie_result.supporters: 
        supporters = movie_result.supporters.split(";") 
    else: 
        supporters = []
    

    #Create Movie Object
    movie = {
        'title_DE': movie_result.title_DE,
        'title_EN': movie_result.title_EN,
        'release_date': release_date, 
        'isReleased': isReleased,
        'format': format,
        'isColored': isColored,
        'language': language,
        'duration': duration,

        'synopsis': synopsis,
        'awards': awards,
        'screenings': screenings,
        'supporters': supporters,

        'directors': directors,
        'producers': producers,
        'executive_producers': executive_producers,
        'editors': editors,
        'cinematography': cinematography,
        'sound_recordist': sound_recordist,
        'sound_mix': sound_mix,
        'color': color,
        'image_url' : movie_result.image_url
    }

    print(movie)

    return render_template('movie.html',movie=movie)

# @app.route('/show/<filename>')
# def uploaded_file(filename):
#     filename = 'http://127.0.0.1:5000/uploads/' + filename
#     return render_template('template.html', filename=filename)

@app.route('/edit_movie', methods=['GET', 'POST'])
@login_required
def edit_movie():
    
    form = PostMovieForm()
        # filename = request.files.get('photo')
        # photos.save(filename)

    form.directors.choices = [(director.id, director.name) for director in Contact.query.all()]
    form.producers.choices = [(producer.id, producer.name) for producer in Contact.query.all()]
    form.executive_producers.choices = [(producer.id, producer.name) for producer in Contact.query.all()]
    form.editors.choices = [(producer.id, producer.name) for producer in Contact.query.all()]
    form.cinematography.choices = [(producer.id, producer.name) for producer in Contact.query.all()]
    form.sound_recordist.choices = [(producer.id, producer.name) for producer in Contact.query.all()]
    form.sound_mix.choices = [(producer.id, producer.name) for producer in Contact.query.all()]
    form.color.choices = [(producer.id, producer.name) for producer in Contact.query.all()]

     
    if form.validate_on_submit():
        file = request.files['image_url']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            #print(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            imageIncluded = True
            e = {
                'title_DE': form.data['title_DE'],
                'title_EN': form.data['title_EN'],
                'release_date': form.data['release_date'], 
                'isReleased': form.data['isReleased'],
                'image_url' :  str(url_for('static', filename= 'movies/' + filename)),
                'format': form.data['format'],
                'isColored': form.data['isColored'],
                'language': form.data['language'],
                'duration': form.data['duration'],

                'synopsis': form.data['synopsis'],
                'awards': form.data['awards'],
                'screenings': form.data['screenings'],
                'supporters': form.data['supporters'],

                'directors': form.data['directors'],
                'producers': form.data['producers'],
                'executive_producers': form.data['executive_producers'],
                'editors': form.data['editors'],
                'cinematography': form.data['cinematography'],
                'sound_recordist': form.data['sound_recordist'],
                'sound_mix': form.data['sound_mix'],
                'color': form.data['color'] 
            }
            Movie.addMovie(e, imageIncluded)
            flash('Your changes have been saved.')
        else:
            imageIncluded = False
            e = {
                'title_DE': form.data['title_DE'],
                'title_EN': form.data['title_EN'],
                'release_date': form.data['release_date'], 
                'isReleased': form.data['isReleased'],
                #'image_url' :  str(url_for('static', filename= 'movies/' + filename)),
                'format': form.data['format'],
                'isColored': form.data['isColored'],
                'language': form.data['language'],
                'duration': form.data['duration'],

                'synopsis': form.data['synopsis'],
                'awards': form.data['awards'],
                'screenings': form.data['screenings'],
                'supporters': form.data['supporters'],

                'directors': form.data['directors'],
                'producers': form.data['producers'],
                'executive_producers': form.data['executive_producers'],
                'editors': form.data['editors'],
                'cinematography': form.data['cinematography'],
                'sound_recordist': form.data['sound_recordist'],
                'sound_mix': form.data['sound_mix'],
                'color': form.data['color'] 
            }
            Movie.addMovie(e, imageIncluded)
            flash('Your changes have been saved.')  
        #print(e)

        return redirect(url_for('edit_movie'))
    elif request.method == 'GET':
        id = request.args.get("id")
        if id is not None: 
            print(id)
            movie = Movie.getMovie(int(id))
            form.title_DE.data = movie.title_DE
            form.title_EN.data = movie.title_EN
            form.isReleased.data = movie.isReleased
            form.release_date.data = movie.release_date
            form.format.data = movie.format
            form.isColored.data = movie.isColored
            form.language.data = movie.language
            form.duration.data = movie.duration

            form.synopsis.data = movie.synopsis
            form.awards.data = movie.awards
            form.screenings.data = movie.screenings
            form.supporters.data = movie.supporters

            # form.directors.data = movie.directors
            # form.producers.data = movie.producers
            # form.executive_producers.data = movie.executive_producers
            # form.editors.data = movie.editors
            # form.cinematography.data = movie.cinematography
            # form.sound_recordist.data = movie.sound_recordist
            # form.sound_mix.data = movie.sound_mix
            # form.color.data = movie.color
       
    return render_template('edit.html', title='Edit Movie',form=form)

@app.route ('/delete_movie')
def delete_movie():
    id = int(request.args.get("id"))
    Movie.deleteMovie(id)
    return redirect(url_for('dashboard'))

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

####################### Dashboard    ##############################
@app.route ('/dashboard_contacts')
def dashboard_contacts():
    contacts = Contact.query.all()
    return render_template('dashboard_contacts.html',contacts=contacts)

@app.route ('/dashboard_news')
def dashboard_news():
    posts = Post.query.all()
    return render_template('dashboard_news.html',posts=posts)

@app.route('/dashboard_info',  methods=['GET', 'POST'])
def dashboard_info():
    about_users = User.get_about()
    #general = User.get_general()
    #print(general)
    form = AboutContactForm()
    form.about_contacts.choices = [(user.id, user.username) for user in User.query.all()]
    if form.validate_on_submit():
        file = request.files['upload_file']
        if file and allowed_file(file.filename):
            #filename = secure_filename(file.filename)
            filename = 'About.txt'
            #print(os.path.join(app.config['UPLOAD_FOLDER_ABOUT'], filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER_ABOUT'], filename))
        print(form.data['about_contacts'])
        User.update_about_status(form.data['about_contacts'])
        about_users = User.get_about()
        #general = User.get_general()
    return render_template('dashboard_info.html',form=form, about_users=about_users)

@app.route('/dashboard_design',  methods=['GET', 'POST'])
def dashboard_design():
    form = UploadForm()
    if form.validate_on_submit():
        folder_name = request.form['sections']
        #target = os.path.join(app.config['UPLOAD_FOLDER_HEADER'], '{}'.format(folder_name))
        target = os.path.join(app.config['UPLOAD_FOLDER_HEADER'], folder_name)

        #print(target)

        if not os.path.isdir(target):
            os.mkdir(target)
            
        file = request.files['image_url']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(target, filename))

            e = {
                'section' : folder_name,
                #'image_url' :  (os.path.join(target, filename))
                #'image_url' :  str(url_for('static', filename= 'movies/' + filename)),
                'image_url' :  str(url_for('static', filename= 'header/{}/'.format(folder_name) + filename)),
                'current' : 1

            }
        
            #print(e['image_url'])
            DesignImage.addDesignImage(e)
    return render_template("dashboard_design.html", form = form)

####################### IMAGE UPLOAD src: https://gist.github.com/greyli/ca74d71f13c52d089a8da8d2b758d519 ##############################

# photos = UploadSet('photos', IMAGES)
# configure_uploads(app, photos)
# patch_request_class(app)  # set maximum file size, default is 16MB

# class UploadForm(FlaskForm):
#     photo = FileField(validators=[FileAllowed(photos, u'Image Only!'), FileRequired(u'Choose a file!')])
#     submit = SubmitField(u'Upload')

# @app.route('/upload', methods=['GET', 'POST'])
# def upload_file():
#     form = UploadForm()
#     if form.validate_on_submit():
#         for filename in request.files.getlist('photo'):
#             photos.save(filename)
#         success = True
#     else:
#         success = False
#     return render_template('upload.html', form=form, success=success)

# @app.route('/manage')
# def manage_file():
#     files_list = os.listdir(app.config['UPLOADED_PHOTOS_DEST'])
#     return render_template('manage.html', files_list=files_list)


# @app.route('/delete/<filename>')
# def delete_file(filename):
#     file_path = photos.path(filename)
#     os.remove(file_path)
#     return redirect(url_for('manage_file'))

# @app.route('/open/<filename>')
# def open_file(filename):
#     file_url = photos.url(filename)
#     return render_template('browser.html', file_url = file_url, filename = filename)