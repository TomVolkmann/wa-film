from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

UPLOAD_FOLDER = 'app\static\movies'

app = Flask(__name__)
app.config.from_object(Config)
app.config['UPLOADED_PHOTOS_DEST'] = 'app\static\movies'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
bootstrap = Bootstrap(app)

from app import routes, models,errors