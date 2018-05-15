import os
#import myenviron
import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, render_template, request, url_for, Response
from db import db
from db import User, Recipe, Ingredient, Method, Rating
import csv
import re
import sys


app = Flask(__name__)
app.config.from_pyfile('settings.cfg')
db.init_app(app)
"""---------------------------------FUNCTIONS TO BE MOVED INTO CLASSES IN SEPERATE FILES---------------------------------"""
def export():
    recipes = Recipe.query.all()
    with open('static/export_recipes.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Name", "Description", "Cookingtime", "Servings", "Course", "CountryOfOrigin"])
        for recipe in recipes:
            writer.writerow([recipe.name, recipe.description, recipe.cookingtime, recipe.servings, recipe.course, recipe.countryOfOrigin])


"""---------------------------------Users---------------------------------"""
def add_user(user_values):
    user = User(first=user_values['first'], 
                last=user_values['last'], 
                username=user_values['username'], 
                email=user_values['email'], 
                password=user_values['password'])
    db.session.add(user)
    db.session.commit()

"""---------------------------------Browse recipes---------------------------------"""

def search_recipes(recipe):
    rating = get_rating(1)
    cookingTime=recipe['cookingTime']
    servings=recipe['servings']
    course=recipe['course']
    origin=recipe['origin']
    ingredients = recipe['ingredients-list'].split(',')
    filters = []

    if cookingTime != "":
        filters.append(Recipe.cookingtime==cookingTime)
        
    if servings != "":
        filters.append(Recipe.servings==servings)
        
    if course != "":
       filters.append(Recipe.course==course)
        
    if origin != "":
        filters.append(Recipe.countryOfOrigin==origin)
        
    if ingredients != [""]:
       filters.append( Ingredient.name.in_( ingredients))

    filter_group =tuple(filters)

    if rating:
        query = Recipe.query.join(Recipe.ingredients).join(Recipe.ratings).filter(*filter_group).order_by(Rating.rating.desc()).all()
    else:
        query = Recipe.query.join(Recipe.ingredients).filter(*filter_group).all()




    return query

def favourite_recipe_add(recipeId, username):
    user =search_for_existing(username)
    rating = Rating.query.filter_by(user_id=user.userId).first()

    if rating:
        if rating.rating == 0:
            rating.rating += 1
            db.session.commit()
        else:
            rating.rating -= 1
            db.session.commit()
    else:
        rating = Rating(rating=1, recipe_id=recipeId, user_id=user.userId)
        db.session.add(rating)
        db.session.commit()


 
"""--------------------------------- Add/edit recipes---------------------------------"""

def send_recipe(user_recipe, username):
    user = User.query.filter_by(username=username).first()
    methods = user_recipe.getlist('step')
    methodNumber = 1
    ingredNumber = 1


    recipe = Recipe(name=user_recipe['name'], 
                    description=user_recipe['description'], 
                    cookingtime=user_recipe['cookingtime'], 
                    servings=user_recipe['servings'], 
                    course=user_recipe['course'], 
                    countryOfOrigin=user_recipe['origin'],
                    user_id=user.userId)
    db.session.add(recipe)

    recipe.methods = []
 
    

    for method in methods:
        method1 = Method(stepNumber=methodNumber, description=method)
        recipe.methods.append(method1); 
        methodNumber += 1

    recipe.ingredients = []
    ingredients = user_recipe['ingredients-list'].split(',')

    for ingredient in ingredients:
        ingredient1 = Ingredient(name=ingredient) 
        recipe.ingredients.append(ingredient1); 
        ingredNumber += 1

    db.session.commit()
    
def update_recipe(user_recipe, username, recipeId):
    user = search_for_existing(username)
    recipe = Recipe.query.filter_by(recipeId = recipeId).first()
    methods = Method.query.filter_by(recipe_id = recipe.recipeId).all()
    ingredients = Ingredient.query.filter_by(recipe_id = recipe.recipeId).all()
    methodNumber = 1
    ingredNumber = 1
    methodsGot = user_recipe.getlist('step')

    for method in methods:
        db.session.delete(method)
    for ingredient in ingredients:
        db.session.delete(ingredient)
    
    #db.session.delete(ingredients)

    recipe.name=user_recipe['name'], 
    recipe.description=user_recipe['description'], 
    recipe.cookingtime=user_recipe['cookingtime'], 
    recipe.servings=user_recipe['servings'], 
    recipe.course=user_recipe['course'], 
    recipe.countryOfOrigin=user_recipe['origin'],
    recipe.user_id=user.userId
    db.session.commit()

    methodsGot = user_recipe.getlist('step')
    recipe.methods = []
 
    

    for methodGot in methodsGot:
        method1 = Method(stepNumber=methodNumber, description=methodGot)
        recipe.methods.append(method1); 
        methodNumber += 1

    recipe.ingredients = []
    ingredientsGot = user_recipe['ingredients-list'].split(',')

    for ingredientGot in ingredientsGot:
        ingredient1 = Ingredient(name=ingredientGot) 
        recipe.ingredients.append(ingredient1); 
        ingredNumber += 1

    db.session.commit()

   

"""---------------------------------queries---------------------------------"""

def search_for_existing(username):
    return User.query.filter_by(username=username).first()

def sign_up(username): 
    existing_user = search_for_existing(username)
    return not existing_user is None

def user_login(user_values): 
    existing_user = search_for_existing(user_values['username'])
    if existing_user != None:
        if existing_user.username == user_values['username']:
            if existing_user.password == user_values['password']:
                return True
    else:
        return False

def search_user_recipes(username):
    user = User.query.filter_by(username=username).first()
    return Recipe.query.filter_by(user_id= user.userId).all()



def search_user_methods(recipeId):
    #user = User.query.filter_by(username=username).first()
    return Method.query.filter_by(recipe_id=recipeId).all()

def search_user_ingredients(recipeId):
   # recipe = Recipe.query.filter_by(username=username).first()
    return Ingredient.query.filter_by(recipe_id=recipeId).all()

def get_recipe(recipeId):
    return Recipe.query.filter_by(recipeId= recipeId).first()

def get_rating(recipeId):
    return Rating.query.filter_by(recipe_id= recipeId).first()

def delete_recipe_from_db(recipe, methods, ingredients, rating):

    for method in methods:
        db.session.delete(method)
    for ingredient in ingredients:
        db.session.delete(ingredient)

    db.session.delete(recipe)

    if rating:
        db.session.delete(rating)

    db.session.commit()


"""---------------------------------ROUTES FOR SIGNING UP AND LOGGING IN---------------------------------"""

@app.route('/')
def index():
    return render_template('index.html', user_taken="", wrong_login="")

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        user_values = request.form
        username = user_values['username']
        userExists = sign_up(username)
        print(userExists, file=sys.stderr)
        if userExists:
            return render_template('index.html', user_taken="Sorry, this username was taken. Please try again.", wrong_login="") 
        else:
            add_user(user_values)
            return redirect('my_cookbook/%s'% username)

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        user_values = request.form
        username = user_values['username']
        returning_user = user_login(user_values)
        if returning_user == True:
            return redirect('my_cookbook/%s'% username)
        else:
            return render_template('index.html', user_taken="", wrong_login="Your email or password was incorrect")

"""---------------------------------ROUTES FOR USERS PAGES---------------------------------"""

@app.route('/my_cookbook/<username>')
def my_cookbook(username):
    recipes = search_user_recipes(username)
    return render_template('my_cookbook.html', username=username, recipes=recipes)

@app.route('/<username>/query_recipes')
def query_recipes(username):
    return render_template('query_recipes.html',  username=username, courses=["Starter", "Main", "Dessert"])

@app.route('/<username>/queried_recipes',  methods=['POST'])
def queried_recipes(username):
    if request.method == 'POST':
        recipe = request.form
        recipes = search_recipes(recipe)
        user = search_for_existing(username)
        return render_template('browse_recipes.html',  username=username, recipes=recipes)

@app.route('/<username>/browse_recipes')
def browse_recipes(username):
    return render_template('browse_recipes.html',  username=username, recipes=recipes)

@app.route('/favourite_recipe', methods=['GET'])
def favourite_recipe():
    recipeId = request.args.get('recipe_id')
    username = request.args.get('username')
    favourite_recipe_add(recipeId, username)

@app.route('/<username>/<recipeId>/view_recipe')
def view_recipe(username, recipeId):
    counter=1
    recipe = get_recipe(recipeId)
    methods = search_user_methods(recipeId)
    ingredients = search_user_ingredients(recipeId)
    return render_template('view_recipe.html',  username=username, recipe=recipe, methods=methods, ingredients=ingredients, counter=counter)

@app.route('/<username>/<recipeId>/delete_recipe')
def delete_recipe(username, recipeId):
    recipe = get_recipe(recipeId)
    rating = get_rating(recipeId)
    methods = search_user_methods(recipeId)
    ingredients = search_user_ingredients(recipeId)
    delete_recipe_from_db(recipe, methods, ingredients, rating)
    return redirect('my_cookbook/%s'% username)

@app.route('/<username>/add_recipe')
def add_recipe(username):
    return render_template('add_recipe.html', username=username)

@app.route('/<username>/add_recipe/recipe_created',  methods=['POST'])
def recipe_created(username):
    if request.method == 'POST':
        recipe = request.form
        send_recipe(recipe, username)
        return redirect('my_cookbook/%s'% username) 

@app.route('/<username>/<recipeId>/edit_recipe')
def edit_recipe(username, recipeId):
    counter=0
    recipe = get_recipe(recipeId)
    methods = search_user_methods(recipeId)
    ingredients = search_user_ingredients(recipeId)
    for method in methods:
        counter += 1
    return render_template('edit_recipe.html', username=username, recipe=recipe, methods=methods, ingredients=ingredients, counter=counter)

@app.route('/<username>/<recipeId>/edit_recipe/recipe_updated', methods=['POST'])
def recipe_updated(username, recipeId):
    if request.method == 'POST':
        recipe = request.form
        
        update_recipe(recipe, username, recipeId)
        return redirect('my_cookbook/%s'% username) 

@app.route('/<username>/recipe_stats')
def recipe_stats(username):
    export()
    print("hi", file=sys.stderr)
    return render_template('recipe_stats.html', username=username)

if __name__ == '__main__':
    app.run(host=os.getenv('IP'), port = os.getenv('PORT'), debug=True)











