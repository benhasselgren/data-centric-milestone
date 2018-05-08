import os
from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy


"""-------------------------------DB CONFIG--------------------------------"""

app = Flask(__name__)
app.config.from_pyfile('settings.cfg')
db = SQLAlchemy(app)

class User(db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(50), unique=False, nullable=False)
    last = db.Column(db.String(50), unique=False, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=False, nullable=False)
    #Relationships
    recipe = db.relationship('Recipe', backref='user', lazy=True)
    ingredient = db.relationship('Ingredient', backref='user', lazy=True)

class Recipe(db.Model):
    recipeId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    description = db.Column(db.String(500), unique=False, nullable=False)
    cookingtime = db.Column(db.Integer, unique=False, nullable=False)
    servings = db.Column(db.Integer, unique=False, nullable=False)
    course = db.Column(db.String(20), unique=False, nullable=False)
    countryOfOrigin = db.Column(db.String(50), unique=False, nullable=False)
    #Foreign Key
    user_id = db.Column(db.Integer, db.ForeignKey('user.userId'), nullable=False)
    #Relationships  
    ingredient = db.relationship('Ingredient', backref='recipe', lazy=True)
    rating = db.relationship('Rating', backref='recipe', lazy=True)
    recipe = db.relationship('Method', backref='recipe', lazy=True)

class Ingredient(db.Model):
    ingredientId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    #Foreign Key
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recipeId'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.userId'), nullable=False)

class Rating(db.Model):
    ratingId = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, unique=False, nullable=False)
    #Foreign Key
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recipeId'), nullable=False)

class Method(db.Model):
    methodId = db.Column(db.Integer, primary_key=True)
    stepNumber = db.Column(db.Integer, unique=False, nullable=False)
    description = db.Column(db.String(500), unique=False, nullable=False)
    #Foreign Key
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recipeId'), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

print(User.query.filter_by(username='benhasselgr').first())



