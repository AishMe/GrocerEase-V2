from flask import Flask, jsonify, request
from models import User, db, bcrypt, ma
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
SQLITE_DB_DIR = os.path.join(basedir, "./instance")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + \
    os.path.join(SQLITE_DB_DIR, "store.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'harekrishna'
jwt = JWTManager(app)


# -------------------- MODEL INITIALIZATION -------------------

db.init_app(app)
app.app_context().push()
db.create_all()
bcrypt.init_app(app)
ma.init_app(app)
CORS(app)


# -------------------- ROUTES -------------------

@app.route('/', methods=['GET'])
def get_details():
    return jsonify({'msg': 'hello world'})


@app.route('/add', methods=['POST'])
def add_details():
    email = request.json['email']
    name = request.json['name']
    password = request.json['password']
    role = request.json['role']

    if request.json['avatar'] == '':
        avatar = 'https://www.testhouse.net/wp-content/uploads/2021/11/default-avatar.jpg'
    else:
        avatar = request.json['avatar']

    user_add = User(email=email, name=name, password=password,
                    role=role, avatar=avatar)
    db.session.add(user_add)
    db.session.commit()

    return jsonify({'msg': 'Added Successfully!'})


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

    return jsonify({'access_token': access_token, 'role': user.role, 'msg': f"Successfully Logged In as {user.role.capitalize()}"}), 200


@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    this_user = get_jwt_identity()
    user = User.query.get(this_user['userId'])
    return jsonify({'name': user.name, 'email': user.email, 'avatar': user.avatar, 'msg': 'You are Authorised!'})


@app.route('/delete_acc', methods=['DELETE'])
@jwt_required()
def delete_user():
    this_user = get_jwt_identity()
    # user = User.query.get(this_user['userId'])

    # if user.role != 'admin' and user.user_id != user_id:
    #     return jsonify({'message': 'Unauthorized to delete this user'}), 403

    user_to_delete = User.query.get(this_user['userId'])
    if not user_to_delete:
        return jsonify({'message': 'User not found'}), 404

    db.session.delete(user_to_delete)
    db.session.commit()

    return jsonify({'message': 'User deleted successfully'}), 200


@app.route('/edit_profile', methods=['PUT'])
@jwt_required()
def edit_user():
    this_user = get_jwt_identity()
    # user = User.query.get(this_user['userId'])

    # if user.role != 'admin' and user.user_id != user_id:
    #     return jsonify({'message': 'Unauthorized to edit this user'}), 403

    user_to_edit = User.query.get(this_user['userId'])
    if not user_to_edit:
        return jsonify({'message': 'User not found'}), 404

    data = request.json

    if 'name' in data:
        user_to_edit.name = data['name']

    if 'email' in data:
        user_to_edit.email = data['email']

    if 'password' in data:
        user_to_edit.password = bcrypt.generate_password_hash(
            data['password']).decode('utf-8')

    if 'role' in data:
        user_to_edit.role = data['role']

    db.session.commit()

    return jsonify({'message': 'User information updated successfully'}), 200


if __name__ == "__main__":
    app.run(debug=True)
