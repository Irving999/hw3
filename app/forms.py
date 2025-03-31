from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import Email, EqualTo, DataRequired, Length, ValidationError
import sqlalchemy as sa
from app import db
from app.models import User

# Login form with fields for username, password, and submit button
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=4, max=35)])
    submit = SubmitField("Sign in")
    remember_me = BooleanField("Remember Me")

# Recipe form with fields for title, description, ingredients, and instructions
class RecipeForm(FlaskForm):
    title = StringField('Recipe', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    ingredients = TextAreaField('Ingredients', validators=[DataRequired()])
    instructions = TextAreaField('Instructions', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Registration form with fields for username, email, password, and password confirmation
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField("Re-Enter Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    # Validates username to check if it already exists
    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError('Username already taken')
    
    # Validates email to check if it already exists
    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError('Email already registered. Use a different email.')
