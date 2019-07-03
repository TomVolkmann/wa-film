from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

UPLOAD_FOLDER = 'app\static\movies'
UPLOAD_FOLDER_HEADER = 'app\static\header'
UPLOAD_FOLDER_ABOUT = 'app\static\\about'


app = Flask(__name__)
app.config.from_object(Config)
#app.config['UPLOADED_PHOTOS_DEST'] = 'app\static\movies'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_HEADER'] = UPLOAD_FOLDER_HEADER
app.config['UPLOAD_FOLDER_ABOUT'] = UPLOAD_FOLDER_ABOUT
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
bootstrap = Bootstrap(app)

from app import routes, models,errors