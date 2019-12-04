#imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#make new flask app
app = Flask(__name__)

SECRET_KEY = ""
SQLALCHEMY_DATABASE_URI = "sqlite:///db/database.sqlite3"

#app key and db location
app.config['SECRET_KEY'] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

#create new db
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
#user
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     public_id = db.Column(db.String(50), unique = True)
#     name = db.Column(db.String(50))
#     password = db.Column(db.String(80))
#     admin = db.Column(db.Boolean)  

# #todo 
# class Todo(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     text = db.Column(db.String(50))
#     complete = db.Column(db.Boolean)
#     user_id = db.Column(db.Integer)

@app.route('/<name>')
def index(name):
    user = User(name = name)
    db.session.add(user)
    db.session.commit()
    return '<h1>Added New User!</h1>'


if __name__ == '__main__'  :
    app.run(debug=True)