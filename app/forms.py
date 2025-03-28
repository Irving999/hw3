from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators, TextAreaField

class LoginForm(FlaskForm):
    username = StringField('USERNAME', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.Length(min=4, max=35)])
    submit =  SubmitField("Sign in")
    remember_me = BooleanField("Remember Me")

class RecipeForm(FlaskForm):
    title = StringField('Recipe', validators=[validators.DataRequired()])
    description = TextAreaField('Description', validators=[validators.DataRequired()])
    ingredients = TextAreaField('Ingredients', validators=[validators.DataRequired()])
    instructions = TextAreaField('Instructions', validators=[validators.DataRequired()])
    submit =  SubmitField("Submit")
    