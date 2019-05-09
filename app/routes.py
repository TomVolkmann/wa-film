from app import app
from app import render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired
import main
import database

app.secret_key = "your secret"

class PostMovieForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    release_date = StringField('Release date', validators=[DataRequired()])

@app.route('/')
def show_entries(): 
    form = PostMovieForm() 
    return render_template('show_entries.html', form=form)

@app.route("/index")
def index():
    return render_template('helloWorld.html') 

@app.route ('/add_entry', methods=['POST'])
def add_entry():
    form = PostMovieForm() 

    if form.validate():
        e = {
            'title': form.data['title'],
            'release_date': form.data['release_date']
        }
        print(e)
        database.saveNewMovie(e)
    return redirect('/')


#@app.route('/index')
#def index():
#    return render_template('helloWorld.html') 


#@app.route('/movies')
#def print_movies():
#    movies = database.getMovies()
#    return render_template('list.html', movies = movies) 


