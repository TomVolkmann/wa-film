from app import app
from app import render_template, request, redirect
import database
 
@app.route('/')
@app.route('/index')
def index():
    return render_template('helloWorld.html') 


@app.route ('/add_entry', methods =['POST'])
def add_entry () :
    title = request.form ['title']
    id = request.form ['id']
    new_entry = {
        'title': title,
        'id' : id
    }
    print(new_entry["title"] + " Success")
    database.saveNewMovie(id,title)
    return redirect('/')

@app.route('/movies')
def print_movies():
    movies = database.getMovies()
    return render_template('list.html', movies = movies) 