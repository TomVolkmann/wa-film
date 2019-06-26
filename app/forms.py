from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
from flask_wtf.file import FileField, FileRequired, FileAllowed

class PostMovieForm(FlaskForm):
    title_DE = StringField("Movie Title German", validators=[DataRequired()])
    title_EN = StringField("Movie Title English", validators=[DataRequired()])
    isReleased = BooleanField("Is Released ?")
    release_date = StringField()
    format = StringField()
    isColored = BooleanField("Color or Black and White ?")
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

    #image_url = FileField(validators=[FileRequired(u'Choose a file!')])
    image_url = FileField()

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

class PostNewsForm(FlaskForm):
    title = StringField("News Post Title", validators=[DataRequired()])
    body = StringField("Post body", validators=[DataRequired()])

