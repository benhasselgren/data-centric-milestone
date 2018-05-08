import os
#import myenviron
import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, render_template, request
from db import db
from db import User

app = Flask(__name__)

def search_for_existing(username):
    User.query.filter_by(username=username).first()

def find_existing_user(user_values):
    existing_user = User.query.filter_by(username=user_values['username']).first()
    return existing_user


def sign_up(username): 
    existing_user = search_for_existing(username)
    if existing_user == none:
        return True
    else:
        return False

def user_login(user_values): 
    existing_user = get_existing_user(user_values)
    if existing_user != none:
        if existing_user.username == user_values['username']:
            if existing_user.password== user_values['password']:
                return True
    else:
        return False

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html', user_taken="", wrong_login="")

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        user_values = request.form
        username = user_values['username']
        new_user = sign_up(username)
        if new_user == True:
            return redirect('my_cookbook/%s'% username)
        else:
            return redirect('index.html', user_taken="Sorry, this username was taken. Please try again.", wrong_login="") 

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        user_values = request.form
        username = user_values['username']
        returning_user = user_login(user_values)
        if returning_user == True:
            return redirect('my_cookbook/%s'% username)
        else:
            return redirect('index.html', user_taken="", wrong_login="Your email or password was incorrect")

@app.route('/my_recipme/<username>')
def my_recipme(username):
    return render_template('my_cookbook.html', username=username)

if __name__ == '__main__':
    app.run(host=os.getenv('IP'), port = os.getenv('PORT'), debug=True)