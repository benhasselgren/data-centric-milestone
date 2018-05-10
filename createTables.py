#from flask_sqlalchemy import SQLAlchemy
#from flask import Flask
#from db import User, Recipe, Ingredient, Method

"""-------------------------------Create Tables--------------------------------"""
#app = Flask(__name__)
#app.config.from_pyfile('settings.cfg')
import db
db.drop_all()
db.create_all()

admin = User(first='Ben', 
			 last='Hasselgren',
			 username='benhasselgren',
			 email='admin@example.com',
			 password='lol')

db.session.add(admin)
db.session.commit()



