from flask import Flask, jsonify, request
from models import User, db, bcrypt, ma
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
SQLITE_DB_DIR = os.path.join(basedir, "./instance")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "store.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'harekrishna'
jwt = JWTManager(app)


#-------------------- MODEL INITIALIZATION -------------------

db.init_app(app)
app.app_context().push()
db.create_all()
bcrypt.init_app(app)
ma.init_app(app)
CORS(app)


#-------------------- ROUTES -------------------

@app.route('/', methods=['GET'])
def get_details():
    return jsonify({'msg': 'hello world'})

@app.route('/add', methods=['POST'])
def add_details():
    email = request.json['email']
    name = request.json['name']
    password = request.json['password']
    role = request.json['role']

    user_add = User(email=email, name=name, password=password, role=role)
    db.session.add(user_add)
    db.session.commit()

    return jsonify({ 'msg':'Added Successfully!' })


@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({'message': 'Wrong Username or Password'}), 401

    access_token = create_access_token(identity={
                                       'userId': user.user_id, 
                                       'useremail': user.email, 
                                       'role': user.role
                                       })

    return jsonify({ 'access_token': access_token, 'role': user.role, 'msg': f"Successfully Logged In as {user.role.capitalize()}" }), 200


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    this_user = get_jwt_identity()
    user = User.query.get(this_user['userId'])
    return jsonify({ 'name':user.name, 'msg':'You are Authorised!' })


if __name__ == "__main__":
    app.run(debug=True)