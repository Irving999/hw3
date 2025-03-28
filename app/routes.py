from app import myapp_obj
from flask import render_template
from flask import redirect
from app.forms import LoginForm
from app.forms import RecipeForm
from app.models import User
from app.models import Recipe
from app import db
import sqlalchemy as sa

# from <X> import <Y>

@myapp_obj.route("/")
@myapp_obj.route("/recipes")
def show_recipes():
    recipes = Recipe.query.all()
    return render_template("all_recipes.html", recipes=recipes)

@myapp_obj.route("/recipe/<integer>")
def show_recipe(integer):
    recipe = Recipe.query.get_or_404(integer)
    return render_template("recipe_details.html", recipe=recipe)

@myapp_obj.route("/recipe/<integer>/delete", methods=['GET'])
def delete_recipe(integer):
    recipe = Recipe.query.get_or_404(integer)
    db.session.delete(recipe)
    db.session.commit()
    return render_template("recipe_deleted.html")
    

@myapp_obj.route("/recipe/new", methods=['GET', 'POST'])
def new_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(title=form.title.data, 
                            description=form.description.data,
                            ingredients=form.ingredients.data,
                            instructions=form.instructions.data)
        db.session.add(recipe)
        db.session.commit()
        return redirect("/")
    return render_template("new_recipe.html", form=form)