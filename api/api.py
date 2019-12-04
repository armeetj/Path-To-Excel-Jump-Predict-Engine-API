#==============================
#           IMPORTS
#==============================
from flask import Flask, request, make_response 
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import json
import jwt
import datetime
import secrets

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
    name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)  

#todo 
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(50))
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)

#==============================
#         TOKEN WORK
#==============================
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token
            return json.dumps({'message': 'token is missing'}), 401

        try:
            data = 'token'
            current_user = User.query.filter_by(public_id=data['public_id']).first() 
        except:
            return json.dumps({'message': 'invalid token'}), 401

        return f(current_user, *args, **kwargs)
    return decorated

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
@token_required
def get_all_users(current_user):
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
@app.route('/api/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(current_user,public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        response = {"message": "no user found"}
        return json.dumps(response)

    response_dict =[]
    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin
    response_dict.append(user_data)
    response = json.dumps(response_dict)
    return response

#POST   /user/
@app.route('/api/user', methods=['POST'])
@token_required
def create_user(current_user):
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
@app.route('/api/user/<public_id>', methods=['PUT'])
@token_required
def promote_user(current_user,public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        response = {"message": "no user found"}
        return json.dumps(response)
    user.admin = True
    db.session.commit()

    response = {"message": "user promoted to admin"}
    response = json.dumps(response)
    return response

#DELETE /user/username
@app.route('/api/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user,public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        response = {"message": "no user found"}
        return json.dumps(response)
    db.session.delete(user)
    db.session.commit()

    response = {"message": "user has been deleted"}
    response = json.dumps(response)
    return response

#GET /auth
@app.route('/api/auth')
@token_required
def auth(current_user):
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        #return auth
        return make_response('{"message":"Could not verify"}', 401, {'WWW-Authenticate':'Basic realm="login required"'})
    
    user = User.query.filter_by(name=auth.username).first()

    if not user:
        response = {"message": "no user found"}
        return json.dumps(response)

    if check_password_hash(user.password, auth.password):
        response = {"token": 'token'}
        return json.dumps(response)

    return make_response('{"message":"Could not verify"}', 401, {'WWW-Authenticate':'Basic realm="login required"'})

    
#run app 
if __name__ == '__main__'  :
    app.run(debug=True)