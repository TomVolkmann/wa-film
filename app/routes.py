from app import app
from app import render_template, request, redirect
import main
import database
 
@app.route('/')
@app.route('/index')
def index():
    return render_template('helloWorld.html') 


@app.route ('/add_entry', methods =['POST'])
def add_entry () :
    new_entry = {
        'title': request.form['title'],
        'id' : request.form['id']
    }
    main.confirmInput(new_entry)
    return redirect('/')

@app.route('/movies')
def print_movies():
    movies = database.getMovies()
    return render_template('list.html', movies = movies) 


