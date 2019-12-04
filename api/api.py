#==============================
#           IMPORTS
#==============================
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

#==============================
#            CONFIG
#==============================
#make new flask app
app = Flask(__name__)

SECRET_KEY = ""
SQLALCHEMY_DATABASE_URI = "sqlite:///../db/db.db"

#app key and db location
app.config['SECRET_KEY'] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

#create new db
db = SQLAlchemy(app)

#==============================
#         DB CLASSES
#==============================
#user
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    public_id = db.Column(db.String(50), unique = True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)  

#todo 
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(50))
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)

#==============================
#          APP ROUTES
#==============================
#GET    /
@app.route('/', methods=['GET'])
def redirect_to_api():
    return "make requests to /api instead"
@app.route('/api/', methods=['GET'])
def home():
    return "Home Page!"

#GET    /user/
@app.route('/api/user', methods=['GET'])
def get_all_users():
    return 'placeholder'

#GET    /user/username 
@app.route('/api/user/<user_id>', methods=['GET'])
def get_one_user():
    return 'placeholder'

#POST   /user/
@app.route('/api/user', methods=['POST'])
def create_user():
    return 'placeholder'

#PUT    /user/username
@app.route('/api/user/<user_id>', methods=['PUT'])
def promote_user():
    return 'placeholder'

#DELETE /user/username
@app.route('/api/user/<user_id>', methods=['DELETE'])
def delete_user():
    return 'placeholder'

#run app 
if __name__ == '__main__'  :
    app.run(debug=True)