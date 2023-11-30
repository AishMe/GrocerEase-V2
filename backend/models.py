from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from datetime import datetime

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
    request_approval = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, email, name, password, role, avatar):
        self.email = email
        self.name = name
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.role = role
        self.avatar = avatar
        self.request_approval = 0


class Category(db.Model):
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.Text, nullable=False)
    category_approval = db.Column(db.Integer, nullable=True, default=0)
    category_image = db.Column(
        db.String(255), nullable=True, default='/default_img.png')
    products = db.relationship('Product', backref='category', lazy=True)


class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey(
        Category.category_id), nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    manufacturing_date = db.Column(db.Text, default=datetime.now().date(), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    hasDiscount = db.Column(db.String(10), nullable=True)
    product_image = db.Column(
        db.String(255), nullable=True, default='/default_img.png')
    orders = db.relationship('OrderItem', backref='product', lazy=True)


class Favourite(db.Model):
    favourite_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(Product.product_id), nullable=False)


class Cart(db.Model):
    cart_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(Product.product_id), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)


class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        User.user_id), nullable=False)
    order_date = db.Column(
        db.Text, default=datetime.now().date(), nullable=False)


class OrderItem(db.Model):
    order_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey(
        Order.order_id), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        Product.product_id), nullable=False)
    category_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    order = db.relationship('Order', backref='items', lazy=True)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'email', 'name', 'role', 'avatar')


class OrderSchema(ma.Schema):
    class Meta:
        fields = ('order_id', 'user_id', 'order_date')


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('product_id', 'name', 'price', 'image', 'manufacturing_date')


class OrderItemSchema(ma.Schema):
    class Meta:
        fields = ('order_item_id', 'order_id',
                  'product_id', 'quantity', 'total_price')


user_schema = UserSchema()
