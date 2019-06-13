from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class PostMovieForm(FlaskForm):
    title_DE = StringField(validators=[DataRequired()])
    title_EN = StringField(validators=[DataRequired()])
    isReleased = BooleanField(validators=[DataRequired()])
    release_date = StringField()
    format = StringField()
    isColored = BooleanField()
    language = StringField()
    duration = StringField()
    synopsis = StringField()
    awards = StringField()
    screenings = StringField()
    supporters = StringField()
    directors = StringField()
    producers = StringField()
    executive_producers = StringField()
    editors = StringField()
    cinematography = StringField()
    sound_recordist = StringField()
    sound_mix = StringField()
    color = StringField()

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')