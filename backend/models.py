from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()
ma = Marshmallow()


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.Text, nullable=False)
    avatar = db.Column(db.Text, nullable=True)

    def __init__(self, email, name, password, role, avatar):
        self.email = email
        self.name = name
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.role = role
        self.avatar = avatar


class UserSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'email', 'name', 'role', 'avatar')


user_schema = UserSchema()
