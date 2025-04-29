from app import myapp_obj
from app.forms import LoginForm, RecipeForm, RegistrationForm
from app.models import User, Recipe
from app import db
from flask import redirect, render_template, request, flash, url_for
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from urllib.parse import urlsplit

# Shows current user, if logged in, recipes
@myapp_obj.route("/recipes")
@login_required
def show_recipes():
    recipes = Recipe.query.filter_by(user_id=current_user.id).all()
    return render_template("all_recipes.html", recipes=recipes)

# Shows all users and their recipe regardless if logged in or not
@myapp_obj.route("/")
@myapp_obj.route("/home")
def home():
    users = User.query.all()
    return render_template("home.html", users=users)

# Shows more details of a specific recipe
@myapp_obj.route("/recipe/<integer>")
@login_required
def show_recipe(integer):
    recipe = Recipe.query.get_or_404(integer)
    return render_template("recipe_details.html", recipe=recipe)

# Url that deletes recipe 
@myapp_obj.route("/recipe/<integer>/delete", methods=['GET'])
@login_required
def delete_recipe(integer):
    recipe = Recipe.query.get_or_404(integer)
    if recipe.user_id != current_user.id:
        flash('You can only delete your own recipes.')
        return redirect(url_for('show_recipes'))
    db.session.delete(recipe)
    db.session.commit()
    return render_template("recipe_deleted.html")

# Login page to sign in 
@myapp_obj.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('show_recipes'))
    
    form = LoginForm()
        
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('show_recipes')
        return redirect(next_page)
    return render_template("login.html", title="Login", form=form)

# Logs out current user
@myapp_obj.route("/logout")
def logout():
    logout_user()
    return redirect("login")

# Register page
@myapp_obj.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('recipes'))
    
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a user!')
        return redirect(url_for('login'))
    return render_template("register.html", title='Register', form=form)

# Page to create new recipes
@myapp_obj.route("/recipe/new", methods=['GET', 'POST'])
@login_required
def new_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(
            title=form.title.data, 
            description=form.description.data,
            ingredients=form.ingredients.data,
            instructions=form.instructions.data,
            user_id=current_user.id
            )
        db.session.add(recipe)
        db.session.commit()
        return redirect("/")
    return render_template("new_recipe.html", form=form)