from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField,SelectMultipleField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User, Contact

class PostMovieForm(FlaskForm):
    title_DE = StringField("Movie Title German", validators=[DataRequired()])
    title_EN = StringField("Movie Title English", validators=[DataRequired()])
    isReleased = BooleanField("Is Released ?")
    release_date = StringField()
    format = StringField()
    isColored = SelectField('Color',choices=[('Col', 'Color'), ('b_w', 'Black & White')])
    language = StringField()
    duration = StringField()

    synopsis = TextAreaField()
    awards = StringField()
    screenings = StringField()
    supporters = StringField()

    directors = SelectMultipleField(choices=[], coerce=int)
    producers = SelectMultipleField(choices=[], coerce=int)
    executive_producers = SelectMultipleField(choices=[], coerce=int)
    editors = SelectMultipleField(choices=[], coerce=int)
    cinematography = SelectMultipleField(choices=[], coerce=int)
    sound_recordist = SelectMultipleField(choices=[], coerce=int)
    sound_mix = SelectMultipleField(choices=[], coerce=int)
    color = SelectMultipleField(choices=[], coerce=int)

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

class ContactForm(FlaskForm):
    name = StringField(validators=[DataRequired()])

