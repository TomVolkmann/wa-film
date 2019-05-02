from app import app
from app import render_template

@app.route('/')
@app.route('/index')
def index():
    return render_template('helloWorld.html')