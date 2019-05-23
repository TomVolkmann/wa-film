from flask import Flask, render_template, request, redirect, flash
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)

from app import routes
