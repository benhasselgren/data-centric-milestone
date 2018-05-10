import os
#import myenviron
import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, render_template, request, url_for
from db import db
from db import User, Recipe, Ingredient, Method
import re
import sys


app = Flask(__name__)
app.config.from_pyfile('settings.cfg')
db.init_app(app)
"""---------------------------------FUNCTIONS---------------------------------"""

def add_user(user_values):
    user = User(first=user_values['first'], 
                last=user_values['last'], 
                username=user_values['username'], 
                email=user_values['email'], 
                password=user_values['password'])
    db.session.add(user)
    db.session.commit()

def send_recipe(user_recipe, username):
    user = User.query.filter_by(username=username).first()
    methodNumber = 1
    ingredNumber = 1
    print(user_recipe.items(), file=sys.stderr)
    methods = user_recipe.getlist('step')


    recipe = Recipe(name=user_recipe['name'], 
                    description=user_recipe['description'], 
                    cookingtime=user_recipe['cookingtime'], 
                    servings=user_recipe['servings'], 
                    course=user_recipe['course'], 
                    countryOfOrigin=user_recipe['origin'],
                    user_id=user.userId)
    db.session.add(recipe)
    #ingredient = Ingredient(name=user_recipe[""])

    recipe.methods = []
 
    

    for method in methods:
        method1 = Method(stepNumber=methodNumber, description=method)
        recipe.methods.append(method1); 
        #db.session.add(method1)
        methodNumber += 1

    recipe.ingredients = []
    ingredients = user_recipe['ingredients-list'].split(',')

    for ingredient in ingredients:
        ingredient1 = Ingredient(name=ingredient) 
        recipe.ingredients.append(ingredient1); 
        ingredNumber += 1

    db.session.commit()
    



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
    return render_template('my_cookbook.html', username=username)

@app.route('/<username>/add_recipe')
def add_recipe(username):
    return render_template('add_recipe.html', username=username)

@app.route('/<username>/add_recipe/recipe_created',  methods=['POST'])
def recipe_created(username):
    if request.method == 'POST':
        recipe = request.form
        print(recipe, file=sys.stderr)
        send_recipe(recipe, username)
        return redirect('my_cookbook/%s'% username) 

if __name__ == '__main__':
    app.run(host=os.getenv('IP'), port = os.getenv('PORT'), debug=True)











