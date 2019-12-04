#==============================
#           IMPORTS
#==============================
from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import json

#==============================
#            CONFIG
#==============================
#make new flask app
app = Flask(__name__)

SECRET_KEY = "secret"
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
    users = User.query.all()
    response_dict = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        response_dict.append(user_data)
    
    response = json.dumps(response_dict)
    return response

#GET    /user/username 
@app.route('/api/user/<user_id>', methods=['GET'])
def get_one_user():
    return 'placeholder'

#POST   /user/
@app.route('/api/user', methods=['POST'])
def create_user():
    #get request json
    data = request.get_json()

    #generate a password for the user
    hashed_password = generate_password_hash(data['password'], method = "sha256")

    #add user to the db
    new_user = User(public_id=str(uuid.uuid4()), name=data["name"], password = hashed_password, admin = False)
    db.session.add(new_user)
    db.session.commit()

    response = {"message":"new user created"}
    return json.dumps(response)

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