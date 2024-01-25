from models import User, Cart, Favourite, Order, OrderItem, Product, Category, Rating, db, bcrypt, ma
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from textblob import TextBlob
from flask import Flask, jsonify, request, send_file, redirect
from monthly_report import generate_pdf_report
from tasks import export_product_data_to_csv, send_reset_email
from flask_caching import Cache
from functools import wraps
from flask_cors import CORS
from sqlalchemy import or_
from datetime import date
import numpy as np
import regex as re
import time
import os
from itsdangerous import URLSafeTimedSerializer

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
SQLITE_DB_DIR = os.path.join(basedir, "./instance")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + \
    os.path.join(SQLITE_DB_DIR, "store.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'harekrishna'
jwt = JWTManager(app)


cache = Cache(config={
    "DEBUG": True,
    "CACHE_TYPE": "RedisCache",
    "CACHE_KEY_PREFIX": "grocery_store_mad2",
    "CACHE_REDIS_URL": "redis://localhost:6379/1",
    "CACHE_DEFAULT_TIMEOUT": 300
})


# -------------------- MODEL INITIALIZATION -------------------

db.init_app(app)
app.app_context().push()
db.create_all()
bcrypt.init_app(app)
ma.init_app(app)
CORS(app)
cache.init_app(app)


# -------------------- RBAC DECORATOR -----------------------


def role_required(roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_user = get_jwt_identity()
            # Assuming 'role' is included in JWT
            user_role = current_user.get('role')

            if user_role not in roles:
                return jsonify({'message': 'Access Denied. Insufficient permissions.'}), 403

            return func(*args, **kwargs)
        return wrapper
    return decorator


# -------------------- ROUTES -------------------

@app.route('/', methods=['GET'])
def get_details():
    return jsonify({'msg': 'hello world'})


@app.route('/api/user/register', methods=['POST'])
def add_details():
    email = request.json['email']
    name = request.json['name']
    password = request.json['password']
    role = request.json['role']

    request_approval = 0

    user = db.session.query(User).filter_by(email=email).first()
    if user:
        return jsonify({'msg': 'This email already exists. Please try to sign up with another email id.'})

    else:
        if (role == 'user' or role == 'admin'):
            request_approval = 1
        elif role == 'manager':
            request_approval = 0

        user_add = User(email=email, name=name, password=password,
                        role=role, request_approval=request_approval)
        db.session.add(user_add)
        db.session.commit()

        return jsonify({'msg': 'You have Registered Successfully!'})


@app.route('/api/user/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    user = db.session.query(User).filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({'message': 'Wrong Username or Password'}), 401

    access_token = create_access_token(identity={
                                       'userId': user.user_id,
                                       'useremail': user.email,
                                       'role': user.role
                                       })

    return jsonify({'access_token': access_token, 'role': user.role, 'msg': f"Successfully Logged In as {user.role.capitalize()}"}), 200


@app.route('/api/user/reset_password_request', methods=['POST'])
def reset_password_request():
    email = request.json.get('email')
    password = request.json.get('password')

    user = db.session.query(User).filter_by(email=email).first()
    if user:
        send_reset_email.delay(email, password)
        return jsonify({'message': 'Email has been sent! Please verify your identity by clicking on the link that has been sent on your email address.'})


@app.route('/api/user/reset_password/<string:new_password>/<string:token>', methods=['GET'])
def reset_with_token(new_password, token):
    serializer = URLSafeTimedSerializer("secret-key")
    try:
        email = serializer.loads(
            token, salt='reset-password-salt', max_age=3600)
        user = User.query.filter_by(email=email).first()
        if user:
            user.password = new_password
            db.session.commit()
            message = "Hurray, you've been verified!\nPassword Updated Successfully!"
        else:
            message = "Oopsie, the link is invalid."
    except:
        message = "The reset link is invalid or has expired."

    return redirect(f'http://localhost:8080/verify_email?message={message}')


@app.route('/api/user/reset_password', methods=['PUT'])
def reset_password():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = db.session.query(User).filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user.password = hashed_password
    db.session.commit()

    return jsonify({'message': 'Password reset successfully!'}), 200


@app.route('/api/user/profile', methods=['GET'])
@jwt_required()
def profile():
    this_user = get_jwt_identity()
    user = db.session.get(User, this_user['userId'])
    return jsonify({'name': user.name, 'email': user.email, 'avatar': user.avatar, 'msg': 'You are Authorised!'})


@app.route('/api/user/delete_account', methods=['DELETE'])
@jwt_required()
def delete_user():
    this_user = get_jwt_identity()

    user_to_delete = db.session.get(User, this_user['userId'])
    if not user_to_delete:
        return jsonify({'message': 'User not found'}), 404

    order_ids_to_delete = [order.order_id for order in db.session.query(Order).filter_by(
        user_id=user_to_delete.user_id)]

    db.session.query(OrderItem).filter(OrderItem.order_id.in_(
        order_ids_to_delete)).delete(synchronize_session=False)

    db.session.query(Cart).filter_by(user_id=user_to_delete.user_id).delete()
    db.session.query(Order).filter_by(user_id=user_to_delete.user_id).delete()

    db.session.commit()

    db.session.delete(user_to_delete)
    db.session.commit()

    return jsonify({'message': 'User deleted successfully'}), 200


@app.route('/api/user/edit_profile', methods=['PUT'])
@jwt_required()
def edit_user():
    this_user = get_jwt_identity()

    user_to_edit = db.session.get(User, this_user['userId'])
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


@app.route('/api/cart/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    try:
        data = request.json
        print("Received Data:", data)
        product_id = data.get('product_id')
        quantity = data.get('quantity')
        user_id = get_jwt_identity().get('userId')

        product = db.session.get(Product, product_id)
        if not product:
            return jsonify({'message': 'Product not found'}), 404

        # Check if the user has an active cart or create a new one
        cart = db.session.query(Cart).filter_by(
            user_id=user_id, product_id=product_id).first()
        if not cart:
            cart = Cart(
                user_id=user_id,
                product_id=product_id,
                quantity=quantity,
                total_price=product.price * quantity
            )
            db.session.add(cart)
        else:
            # If the product is already in the cart, update the quantity
            cart.quantity += quantity
            cart.total_price += product.price * quantity

        db.session.commit()

        return jsonify({'message': 'Product added to cart'}), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Failed to add to cart'}), 500


# Get Cart Info
@app.route('/api/cart', methods=['GET'])
@jwt_required()
def get_cart():
    try:

        user_id = get_jwt_identity().get('userId')
        cart_items = db.session.query(Cart).filter_by(user_id=user_id).all()

        cart_data = []
        for cart_item in cart_items:
            product = db.session.get(Product, cart_item.product_id)
            if product:
                cart_data.append({
                    'id': product.product_id,
                    'name': product.product_name,
                    'qty': cart_item.quantity,
                    'total_price': cart_item.total_price,
                    'image': product.product_image,
                    'price': product.price,
                    'unit': product.unit,
                    'stock': product.stock,
                    'discount': cart_item.discount,
                })

        return jsonify({'cart': cart_data}), 200

    except Exception as e:
        print(f"Error fetching cart data: {str(e)}")
        return jsonify({'message': 'Error fetching cart data'}), 500


# Update cart items
@app.route('/api/cart/update', methods=['PUT'])
@jwt_required()
def update_cart_item():
    try:
        data = request.get_json()
        user_id = get_jwt_identity().get('userId')
        product_id = data.get('product_id')
        new_quantity = data.get('new_quantity')

        cart_item = db.session.query(Cart).filter_by(
            user_id=user_id, product_id=product_id).first()

        product = db.session.query(Product).filter_by(
            product_id=product_id).first()
        if cart_item:
            cart_item.quantity = new_quantity
            cart_item.total_price = product.price * new_quantity
            db.session.commit()

            return jsonify({'message': 'Cart item updated successfully'}), 200
        else:
            return jsonify({'message': 'Cart item not found'}), 404

    except Exception as e:
        print(f"Error updating cart item: {str(e)}")
        return jsonify({'message': 'Error updating cart item'}), 500


# Remove cart items
@app.route('/api/cart/remove', methods=['POST'])
@jwt_required()
def remove_cart_item():
    try:
        data = request.get_json()
        user_id = get_jwt_identity().get('userId')
        product_id = data.get('product_id')

        cart_item = db.session.query(Cart).filter_by(
            user_id=user_id, product_id=product_id).first()
        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()

            return jsonify({'message': 'Cart item removed successfully'}), 200
        else:
            return jsonify({'message': 'Cart item not found'}), 404

    except Exception as e:
        print(f"Error removing cart item: {str(e)}")
        return jsonify({'message': 'Error removing cart item'}), 500


# New Flask route for checkout
@app.route('/api/checkout', methods=['POST'])
@jwt_required()
@role_required(roles=['user'])
def checkout():
    try:
        user_id = get_jwt_identity()['userId']
        cart_items = request.json.get('cart')

        order = Order(user_id=user_id)
        db.session.add(order)
        db.session.commit()

        for item in cart_items:
            product = db.session.get(Product, item['id'])

            if product:
                if product.stock < item['qty']:
                    return jsonify({'message': f'Not enough quantity in stock for product {product.product_name}'}), 400

                order_item = OrderItem(
                    order_id=order.order_id,
                    product_id=product.product_id,
                    category_id=product.category_id,
                    quantity=item['qty'],
                    total_price=(item['price'] * item['qty']) -
                    (item['price'] * item['qty'])*(item['discount']/100)
                )
                db.session.add(order_item)

                product.stock -= item['qty']

                cart = db.session.query(Cart).filter_by(
                    user_id=user_id, product_id=product.product_id).first()
                if cart:
                    db.session.delete(cart)

        db.session.commit()

        return jsonify({'message': 'Checkout successful'}), 200

    except Exception as e:
        print(f"Error during checkout: {str(e)}")
        db.session.rollback()  # Rollback changes in case of an error
        return jsonify({'message': 'Error during checkout', 'error': str(e)}), 500


@app.route('/api/cart/update/discount', methods=['PUT'])
@jwt_required()
@role_required(roles=['user'])
def update_discount():
    try:
        user_id = get_jwt_identity()['userId']

        data = request.json
        discount_code = data['discount']
        item_name, discount_percent = parse_discount_code(discount_code)
        item_name = item_name.lower().replace(' ', '')  # Normalize the item name

        # Reset discount for all items in the user's cart
        carts = Cart.query.filter_by(user_id=user_id).all()
        for cart in carts:
            cart.discount = 0  # Reset discount

        if item_name == 'allproduct':
            carts = Cart.query.filter_by(user_id=user_id).all()
            for cart in carts:
                product = db.session.get(Product, cart.product_id)

                if product:
                    cart.discount = discount_percent
        else:
            carts = Cart.query.filter_by(user_id=user_id).all()
            for cart in carts:
                product = db.session.get(Product, cart.product_id)
                if product and product.product_name.lower().replace(' ', '') == item_name:
                    cart.discount = discount_percent

        db.session.commit()
        return jsonify({'message': 'Discount updated successfully'}), 200

    except Exception as e:
        print(f"Error during checkout: {str(e)}")
        return jsonify({'message': 'Error while applying the discount', 'error': str(e)}), 500


def parse_discount_code(code):
    pattern = r'([A-Za-z\s]+)(\d+)'
    match = re.match(pattern, code)
    item_name = match.group(1).replace('_', ' ').strip().lower()
    discount_percent = int(match.group(2))
    return item_name, discount_percent


@app.route('/api/favourites', methods=['GET'])
@jwt_required()
@role_required(roles=['user'])
def get_favourites():
    try:
        user_id = get_jwt_identity()['userId']

        favourites = db.session.query(
            Favourite).filter_by(user_id=user_id).all()
        favourite_list = []

        for favourite in favourites:
            product = db.session.get(Product, favourite.product_id)

            if product:
                product_data = {
                    'id': product.product_id,
                    'category_id': product.category_id,
                    'name': product.product_name,
                    'manufacturing_date': product.manufacturing_date,
                    'stock': product.stock,
                    'unit': product.unit,
                    'price': product.price,
                    'image': product.product_image,
                    'product_status': product.product_status
                }

                favourite_list.append(product_data)

        response_data = {'fav_products': favourite_list}
        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({'message': 'Error fetching favourite items', 'error': str(e)}), 500


@app.route('/api/favourite/add', methods=['POST'])
@jwt_required()
@role_required(roles=['user'])
def add_to_favourite():
    try:
        data = request.json
        print("Received Data Fav:", data)
        product_id = data.get('product_id')
        user_id = get_jwt_identity()['userId']

        # Check if the product exists
        product = db.session.get(Product, product_id)
        if not product:
            return jsonify({'message': 'Product not found'}), 404

        # Check if the user has already added the product to favourites
        existing_favourite = db.session.query(Favourite).filter_by(
            user_id=user_id, product_id=product_id).first()

        if existing_favourite:
            return jsonify({'message': 'Product already in favourites'}), 400

        # Create a new favourite entry
        favourite = Favourite(user_id=user_id, product_id=product_id)
        db.session.add(favourite)
        db.session.commit()

        return jsonify({'message': 'Product added to favourites'}), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Failed to add to favourites'}), 500


@app.route('/api/favourite/remove', methods=['DELETE'])
@jwt_required()
@role_required(roles=['user'])
def remove_fav():

    try:
        data = request.json
        print("Received Data Remove Fav:", data)
        product_id = data.get('product_id')
        user_id = get_jwt_identity()['userId']

        fav_item_to_remove = db.session.query(Favourite).filter_by(
            user_id=user_id, product_id=product_id).first()
        if not fav_item_to_remove:
            return jsonify({'message': 'Product not found in favourites.'}), 404

        db.session.delete(fav_item_to_remove)
        db.session.commit()

        return jsonify({'message': 'Product removed from favourites!'}), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Failed to remove from favourites'}), 500


@app.route('/api/orders', methods=['GET'])
@jwt_required()
@role_required(roles=['user'])
def get_orders():
    try:
        user_id = get_jwt_identity()['userId']
        orders = db.session.query(Order).filter_by(user_id=user_id).order_by(
            Order.order_date.desc()).all()

        formatted_orders = []

        for order in orders:
            order_items = db.session.query(OrderItem).filter_by(
                order_id=order.order_id).all()
            order_data = {
                'order_id': order.order_id,
                'order_date': order.order_date,
                'categories': []
            }

            category_dict = {}
            for item in order_items:
                product = db.session.get(Product, item.product_id)
                category_name = product.category.category_name

                if category_name not in category_dict:
                    category_dict[category_name] = {
                        'category_name': category_name,
                        'items': []
                    }

                category_dict[category_name]['items'].append({
                    'order_item_id': item.order_item_id,
                    'product_name': product.product_name,
                    'quantity': item.quantity,
                    'total_price': item.total_price
                })

            order_data['categories'] = list(category_dict.values())
            formatted_orders.append(order_data)

        return jsonify({'orders': formatted_orders}), 200

    except Exception as e:
        print(f"Error during fetching orders: {str(e)}")
        return jsonify({'message': 'Error fetching orders', 'error': str(e)}), 500


@app.route('/api/user/ordered_products', methods=['GET'])
@jwt_required()
@role_required(roles=['user'])
def user_orders():
    current_user_id = get_jwt_identity()['userId']

    # Querying for orders made by the user
    orders = Order.query.filter_by(user_id=current_user_id).all()

    # Getting unique product_ids from these orders
    product_ids = set()
    for order in orders:
        order_items = OrderItem.query.filter_by(order_id=order.order_id).all()
        for item in order_items:
            product_ids.add(item.product_id)

    # Fetching product details
    products = []
    for pid in product_ids:
        product = Product.query.get(pid)
        if product:
            products.append({
                'id': product.product_id,
                'category_id': product.category_id,
                'name': product.product_name,
                'manufacturing_date': product.manufacturing_date,
                'stock': product.stock,
                'unit': product.unit,
                'price': product.price,
                'image': product.product_image,
                'avg_review': product.avg_review,
                'product_status': product.product_status,
            })

    return jsonify(products)


# Add a Product to the Database
@app.route('/api/<int:product_id>/rating/add', methods=['POST'])
@jwt_required()
@role_required(roles=['user'])
def add_rating(product_id):

    current_user_id = get_jwt_identity()['userId']

    rating = request.json['rating']
    review = request.json['review']

    rating = Rating(user_id=current_user_id,
                    product_id=product_id, rating=rating, review=review)

    try:
        db.session.add(rating)
        db.session.commit()

        return jsonify({'message': 'Product Added Successfully!'}), 200

    except Exception as e:
        print(e)
        return jsonify({'message': 'Error Adding the Product.', 'error': str(e)}), 500


@app.route('/api/categories', methods=['GET'])
# @cache.cached(timeout=50)
def get_categories():
    try:
        categories = db.session.query(Category).filter(
            or_(Category.category_approval == 1,
                Category.category_approval == -2, Category.category_approval == 0)
        ).filter(Category.category_id != 0).all()
        category_list = []

        for category in categories:
            category_data = {
                'category_id': category.category_id,
                'name': category.category_name,
                'image': category.category_image,
                'category_approval': category.category_approval
            }
            category_list.append(category_data)

        return jsonify({'categories': category_list}), 200
    except Exception as e:
        return jsonify({'message': 'Error fetching categories', 'error': str(e)}), 500


# Add Category
@app.route('/api/category/add', methods=['POST'])
@jwt_required()
@role_required(roles=['admin', 'manager'])
def add_category():

    name = request.json['name']
    image = request.json['image']

    if request.json['image'] == '':
        image = 'https://maxicus.com/wp-content/uploads/2022/05/Virtual-Shopping-A-Step-into-the-Future-of-Retail.png'
    else:
        image = request.json['image']

    user_id = get_jwt_identity()['userId']
    user = db.session.query(User).filter_by(user_id=user_id).first()

    if user.role == 'admin':
        category_approval = 1
    elif user.role == 'manager':
        category_approval = 0

    category = Category(category_name=name, category_image=image,
                        category_approval=category_approval)

    try:
        db.session.add(category)
        db.session.commit()

        return jsonify({'message': 'Category Added Successfully!'}), 200

    except Exception as e:
        return jsonify({'message': 'Error Adding the Category', 'error': str(e)}), 500


# Update Database Record in Category
@app.route('/api/category/edit/<int:category_id>', methods=['PUT'])
@jwt_required()
@role_required(roles=['admin', 'manager'])
def update_category(category_id):
    category_to_update = db.session.query(Category).get_or_404(category_id)
    data = request.json

    try:
        category_to_update.category_name = data['name']
        category_to_update.category_image = data['image']

        if data['image'] == '':
            category_to_update.category_image = 'https://maxicus.com/wp-content/uploads/2022/05/Virtual-Shopping-A-Step-into-the-Future-of-Retail.png'
        else:
            category_to_update.category_image = data['image']

        db.session.commit()
        return jsonify({'message': 'Category Info Updated Successfully!'}), 200

    except Exception as e:
        print(e)
        return jsonify({'message': 'Error Updating the Category', 'error': str(e)}), 500


# Delete a Category and it's Products from the Database
@app.route('/api/category/delete/<int:category_id>', methods=['DELETE'])
@jwt_required()
@role_required(roles=['admin'])
def delete_category(category_id):
    try:

        category_to_delete = db.session.get(Category, category_id)
        if not category_to_delete:
            return jsonify({'message': 'Category not found'}), 404

        products_in_category = db.session.query(
            Product).filter_by(category_id=category_id).all()

        for product in products_in_category:
            delete_product(product.product_id)

        # Check if there are no products or if all products are successfully deleted
        if not products_in_category or not any(product.product_status == 0 for product in products_in_category):
            db.session.delete(category_to_delete)
        else:
            # If products have connections and cannot be directly deleted, update category_approval to -3
            category_to_delete.category_approval = -3

        db.session.commit()

        return jsonify({'message': 'Category and its products deleted or marked for approval'}), 200

    except Exception as e:
        return jsonify({'message': 'Error deleting category and its products', 'error': str(e)}), 500


@app.route('/api/products', methods=['GET'])
# @cache.cached(timeout=50)
def get_products():
    start_time = time.time()
    try:

        products = db.session.query(Product).filter(
            Product.product_id != 0).all()

        product_list = []

        for product in products:
            product_data = {
                'id': product.product_id,
                'category_id': product.category_id,
                'name': product.product_name,
                'manufacturing_date': product.manufacturing_date,
                'stock': product.stock,
                'unit': product.unit,
                'price': product.price,
                'image': product.product_image,
                'avg_review': product.avg_review,
                'product_status': product.product_status,
            }
            product_list.append(product_data)

        end_time = time.time()
        print(f"Time taken: {end_time - start_time} seconds")

        return jsonify({'products': product_list}), 200
    except Exception as e:
        return jsonify({'message': 'Error fetching products', 'error': str(e)}), 500


# Add a Product to the Database
@app.route('/api/<int:category_id>/product/add', methods=['POST'])
@jwt_required()
@role_required(roles=['admin', 'manager'])
def add_product(category_id):

    name = request.json['name']
    price = request.json['price']
    unit = request.json['unit']
    stock = request.json['stock']

    if request.json['image'] == '':
        image = 'https://maxicus.com/wp-content/uploads/2022/05/Virtual-Shopping-A-Step-into-the-Future-of-Retail.png'
    else:
        image = request.json['image']

    product = Product(category_id=category_id, product_name=name,
                      product_image=image, price=price, unit=unit, stock=stock)

    try:
        db.session.add(product)
        db.session.commit()

        return jsonify({'message': 'Product Added Successfully!'}), 200

    except Exception as e:
        return jsonify({'message': 'Error Adding the Product.', 'error': str(e)}), 500


# Update Database Record in Product
@app.route('/api/product/edit/<int:product_id>', methods=['PUT'])
@jwt_required()
@role_required(roles=['admin', 'manager'])
def update_product(product_id):

    product_to_update = db.session.query(Product).get_or_404(product_id)
    data = request.json

    try:
        product_to_update.product_name = data['name']
        product_to_update.price = data['price']
        product_to_update.unit = data['unit']
        product_to_update.stock = data['stock']

        if data['image'] == '':
            product_to_update.product_image = 'https://maxicus.com/wp-content/uploads/2022/05/Virtual-Shopping-A-Step-into-the-Future-of-Retail.png'
        else:
            product_to_update.product_image = data['image']

        db.session.commit()
        return jsonify({'message': 'Product Info Updated Successfully!'}), 200

    except Exception as e:
        return jsonify({'message': 'Error Updating the Product', 'error': str(e)}), 500


# Delete a Product from the Database Record
@app.route('/api/product/delete/<int:product_id>', methods=['DELETE'])
@jwt_required()
@role_required(roles=['admin', 'manager'])
def delete_product(product_id):

    product_to_delete = db.session.get(Product, product_id)
    if not product_to_delete:
        return jsonify({'message': 'Product not found'}), 404

    product_in_cart = db.session.query(
        Cart).filter_by(product_id=product_id).first()
    if product_in_cart:
        db.session.delete(product_in_cart)

    product_reviews = db.session.query(
        Rating).filter_by(product_id=product_id).all()
    if product_reviews:
        db.session.delete(product_reviews)

    # Check if the product is in the favorite or order
    product_in_favorite = db.session.query(Favourite).filter_by(
        product_id=product_id).first()
    product_in_order = db.session.query(
        OrderItem).filter_by(product_id=product_id).first()

    try:
        if product_in_favorite or product_in_order:
            product_to_delete.product_status = 0
        else:
            db.session.delete(product_to_delete)

        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'}), 200

    except Exception as e:
        return jsonify({'message': 'Error deleting the product', 'error': str(e)}), 500


# Show the Categories and Products on the Manager & Admin Dashboard
@app.route('/api/manager_admin_dashboard', methods=['GET'])
@jwt_required()
@role_required(roles=['manager', 'admin'])
# @cache.cached(timeout=50)
def manager_admin_dashboard():
    try:
        categories = db.session.query(Category).order_by(
            Category.category_id).all()
        products_by_category = {}

        for category in categories:
            products = db.session.query(Product).filter_by(
                category_id=category.category_id).filter(Product.product_status != 0).all()

            products_data = []
            for product in products:
                products_data.append({
                    'name': product.product_name,
                    'image': product.product_image,
                    'manufacture_date': product.manufacturing_date,
                    'price': product.price,
                    'unit': product.unit,
                    'stock': product.stock,
                    'avg_review': product.avg_review,
                    'product_id': product.product_id,
                    'category_id': product.category_id
                })

            products_by_category[category.category_id] = products_data

        return jsonify({'productsByCategory': products_by_category}), 200

    except Exception as e:
        return jsonify({'message': 'Error fetching products by category for managers', 'error': str(e)}), 500


# Fetch pending managers
@app.route('/admin/pending/managers', methods=['GET'])
@jwt_required()
@role_required(roles=['admin'])
def get_pending_managers():
    try:

        pending_managers = db.session.query(
            User).filter_by(request_approval=0).all()
        pending_managers_data = [{'user_id': manager.user_id,
                                  'name': manager.name,
                                  'role': manager.role,
                                  'avatar': manager.avatar,
                                  'email': manager.email
                                  } for manager in pending_managers]

        return jsonify({'pendingManagers': pending_managers_data}), 200
    except Exception as e:
        return jsonify({'message': 'Error fetching pending managers', 'error': str(e)}), 500


# Fetch approved managers
@app.route('/admin/approved/managers', methods=['GET'])
@jwt_required()
@role_required(roles=['admin'])
def get_approved_managers():
    try:

        pending_managers = db.session.query(User).filter_by(
            request_approval=1).filter_by(role='manager').all()
        pending_managers_data = [{'user_id': manager.user_id,
                                  'name': manager.name,
                                  'role': manager.role,
                                  'avatar': manager.avatar,
                                  'email': manager.email
                                  } for manager in pending_managers]

        return jsonify({'approvedManagers': pending_managers_data}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Error fetching pending managers', 'error': str(e)}), 500


# Fetch rejected managers
@app.route('/admin/rejected/managers', methods=['GET'])
@jwt_required()
@role_required(roles=['admin'])
def get_rejected_managers():
    try:

        pending_managers = db.session.query(
            User).filter_by(request_approval=-1).all()
        pending_managers_data = [{'user_id': manager.user_id,
                                  'name': manager.name,
                                  'role': manager.role,
                                  'avatar': manager.avatar,
                                  'email': manager.email
                                  } for manager in pending_managers]

        return jsonify({'rejectedManagers': pending_managers_data}), 200
    except Exception as e:
        return jsonify({'message': 'Error fetching pending managers', 'error': str(e)}), 500


# Approve manager request
@app.route('/admin/approve/<int:user_id>', methods=['PUT'])
@jwt_required()
@role_required(roles=['admin'])
def approve_request(user_id):
    try:

        user = db.session.get(User, user_id)
        if user:
            user.request_approval = 1
            user.role = 'manager'
            db.session.commit()
            return jsonify({'message': 'Request approved'}), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'message': 'Error approving request', 'error': str(e)}), 500


# Decline manager request
@app.route('/admin/decline/<int:user_id>', methods=['PUT'])
@jwt_required()
@role_required(roles=['admin'])
def decline_request(user_id):
    try:

        user = db.session.get(User, user_id)
        if user:
            user.request_approval = -1
            user.role = 'Pending'
            db.session.commit()
            return jsonify({'message': 'Request declined'}), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'message': 'Error declining request', 'error': str(e)}), 500


# Revert manager status
@app.route('/admin/revert/<int:user_id>', methods=['PUT'])
@jwt_required()
@role_required(roles=['admin'])
def revert_request(user_id):
    try:

        user = db.session.get(User, user_id)
        if user:
            user.request_approval = 0
            user.role = 'pending'
            db.session.commit()
            return jsonify({'message': 'Action Performed Successfully'}), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'message': 'Error processing request', 'error': str(e)}), 500


# Fetch pending categories
@app.route('/admin/pending_categories', methods=['GET'])
@jwt_required()
@role_required(roles=['admin'])
def get_pending_categories():
    try:

        pending_categories = db.session.query(Category).filter_by(
            category_approval=0).all()
        pending_categories_data = [{'category_id': category.category_id,
                                    'name': category.category_name,
                                    'image': category.category_image,
                                    } for category in pending_categories]

        return jsonify({'pendingCategories': pending_categories_data}), 200
    except Exception as e:
        return jsonify({'message': 'Error fetching pending categories', 'error': str(e)}), 500


# Approve category request
@app.route('/admin/approve_category/<int:category_id>', methods=['PUT'])
@jwt_required()
@role_required(roles=['admin'])
def approve_category_request(category_id):
    try:

        category = db.session.get(Category, category_id)
        if category:
            category.category_approval = 1
            db.session.commit()
            return jsonify({'message': 'Category request approved'}), 200
        else:
            return jsonify({'message': 'Category not found'}), 404
    except Exception as e:
        return jsonify({'message': 'Error approving request', 'error': str(e)}), 500


# Decline category request
@app.route('/admin/decline_category/<int:category_id>', methods=['PUT'])
@jwt_required()
@role_required(roles=['admin'])
def decline_category_request(category_id):
    try:

        category = db.session.get(Category, category_id)
        if category:
            category.category_approval = -1
            db.session.commit()
            return jsonify({'message': 'Category request declined'}), 200
        else:
            return jsonify({'message': 'Category not found'}), 404
    except Exception as e:
        return jsonify({'message': 'Error declining request', 'error': str(e)}), 500


# Fetch items to hard delete them.
@app.route('/admin/hard_delete_item', methods=['GET'])
@jwt_required()
@role_required(roles=['admin'])
def get_hard_delete_items():
    try:

        temp_deleted_products = db.session.query(Product).filter_by(
            product_status=0).all()
        temp_deleted_products_data = [{'id': product.product_id,
                                       'category_id': product.category_id,
                                       'name': product.product_name,
                                       'manufacturing_date': product.manufacturing_date,
                                       'stock': product.stock,
                                       'unit': product.unit,
                                       'price': product.price,
                                       'image': product.product_image,
                                       'product_status': product.product_status,
                                       } for product in temp_deleted_products]

        return jsonify({'tempDeletedProducts': temp_deleted_products_data}), 200
    except Exception as e:
        return jsonify({'message': 'Error fetching temporarily deleted products', 'error': str(e)}), 500


# Delete Products and Their Connections from Favourites and OrderItems
@app.route('/admin/delete_products_and_connections', methods=['POST'])
@jwt_required()
@role_required(roles=['admin'])
def delete_products_and_connections():
    try:

        product_ids = request.json.get('product_ids')

        if not product_ids:
            return jsonify({'message': 'Product IDs are required'}), 400

        for product_id in product_ids:

            favourite_exists = db.session.query(Favourite).filter_by(
                product_id=product_id).first()
            if favourite_exists:
                db.session.query(Favourite).filter_by(
                    product_id=product_id).delete()

            order_items_to_update = db.session.query(OrderItem).filter_by(
                product_id=product_id).all()
            for order_item in order_items_to_update:
                order_item.product_id = 0
                order_item.category_id = 0

        db.session.commit()

        db.session.query(Product).filter(
            Product.product_id.in_(product_ids)).delete()
        db.session.commit()

        return jsonify({'message': 'Products and their connections deleted successfully'}), 200

    except Exception as e:
        print(e)
        return jsonify({'message': 'Error deleting products and their connections', 'error': str(e)}), 500


# Fetch pending categories for deletion request
@app.route('/admin/category_deletion_request', methods=['GET'])
@jwt_required()
@role_required(roles=['admin'])
def get_category_deletion_requests():
    try:

        pending_categories = db.session.query(Category).filter_by(
            category_approval=-2).all()
        pending_categories_data = [{'category_id': category.category_id,
                                    'name': category.category_name,
                                    'image': category.category_image,
                                    } for category in pending_categories]

        return jsonify({'deleteCategories': pending_categories_data}), 200
    except Exception as e:
        return jsonify({'message': 'Error fetching pending categories', 'error': str(e)}), 500


@app.route('/api/edit_category_request/<int:category_id>', methods=['PUT'])
@jwt_required()
@role_required(roles=['manager'])
def update_category_request(category_id):
    category_to_update = db.session.query(Category).get_or_404(category_id)
    data = request.json

    try:
        category_to_update.category_name = data['name']
        category_to_update.category_image = data['image']

        if (data['category_approval']):
            category_to_update.category_approval = data['category_approval']
        else:
            category_to_update.category_approval = 1

        if data['image'] == '':
            category_to_update.category_image = 'https://maxicus.com/wp-content/uploads/2022/05/Virtual-Shopping-A-Step-into-the-Future-of-Retail.png'
        else:
            category_to_update.category_image = data['image']

        db.session.commit()
        return jsonify({'message': 'Category Info Updated Successfully!'}), 200

    except Exception as e:
        print(e)
        return jsonify({'message': 'Error Updating the Category', 'error': str(e)}), 500


# Decline category deletion request (Keep the category)
@app.route('/admin/keep_category/<int:category_id>', methods=['PUT'])
@jwt_required()
@role_required(roles=['admin'])
def decline_category_deletion_request(category_id):
    try:

        category = db.session.get(Category, category_id)
        if category:
            category.category_approval = 1
            db.session.commit()
            return jsonify({'message': 'Category request declined!'}), 200
        else:
            return jsonify({'message': 'Category not found'}), 404
    except Exception as e:
        return jsonify({'message': 'Error declining request', 'error': str(e)}), 500


@app.route('/notification_count', methods=['GET'])
@jwt_required()
def get_notification_count():
    try:

        pending_categories = db.session.query(Category).filter_by(
            category_approval=0).all()
        pending_category_deletion_requests = db.session.query(Category).filter_by(
            category_approval=-2).all()
        pending_managers = db.session.query(
            User).filter_by(request_approval=0).all()

        notification_count = len(
            pending_categories) + len(pending_managers) + len(pending_category_deletion_requests)

        return jsonify({'notificationCount': notification_count}), 200
    except Exception as e:
        return jsonify({'message': 'Error fetching notification count', 'error': str(e)}), 500


# Fetch product-wise sales data
@app.route('/api/product_sales_data', methods=['GET'])
@jwt_required()
@role_required(roles=['manager', 'admin'])
def get_product_sales_data():
    try:
        products = db.session.query(Product).all()

        product_sales_data = {}

        for product in products:
            order_items = db.session.query(OrderItem).filter_by(
                product_id=product.product_id).all()
            total_sales = sum(
                order_item.total_price for order_item in order_items)
            category_name = product.category.category_name
            product_sales_data[product.product_name] = [
                category_name, total_sales]

        return jsonify({'productSalesData': product_sales_data}), 200

    except Exception as e:
        return jsonify({'message': 'Error fetching product-wise sales data', 'error': str(e)}), 500


# Fetch summary cards data
@app.route('/api/card_data', methods=['GET'])
@jwt_required()
@role_required(roles=['manager', 'admin'])
def get_card_data():
    try:
        total_users = db.session.query(User).filter_by(role='user').count()
        out_of_stock_count = db.session.query(
            Product).filter_by(stock=0).count() - 1
        limited_stock_count = db.session.query(Product).filter(
            Product.stock > 0, Product.stock <= 10).count()
        total_products = db.session.query(Product).count()
        total_sales = db.session.query(
            db.func.sum(OrderItem.total_price)).scalar()

        card_data = {
            "Total Users": total_users,
            "Out of Stock": out_of_stock_count,
            "Limited in Stock": limited_stock_count,
            "Total Products": total_products,
            "Total Sales": total_sales if total_sales else 0
        }

        return jsonify({'cardData': card_data}), 200

    except Exception as e:
        return jsonify({'message': 'Error fetching card data', 'error': str(e)}), 500


@app.route('/api/visited_status', methods=['GET'])
def user_visited_status():
    try:

        today_date = date.today()
        print(date.today())
        print(Order.order_date.cast(db.Date))

        orders_today = db.session.query(Order).filter(
            Order.order_date == today_date).all()
        # print(orders_today)
        user_ids_today = set(order.user_id for order in orders_today)

        # Query users who are not in the list of user_ids with orders today
        users = db.session.query(User).filter(User.user_id.notin_(
            user_ids_today), User.role == 'user').all()

        user_names = [user.name for user in users]

        return jsonify(user_names), 200

    except Exception as e:
        return jsonify({'message': 'Error fetching visted status', 'error': str(e)}), 500


@app.route('/download_csv')
def download_csv():
    try:

        export_product_data_to_csv.delay(file_path=basedir+'/product_data.csv')
        file_path = basedir+'/product_data.csv'
        print("FILE PATH: ", file_path)

        if os.path.exists(file_path):
            return send_file(
                file_path,
                mimetype='text/csv',
                download_name="product_data.csv",
                as_attachment=True
            )
        else:
            return "File not found", 404

    except Exception as e:
        return f"Error: {str(e)}", 500
    

@app.route('/api/managers', methods=['GET'])
def fetch_manager_emails():
    managers = User.query.filter(or_(User.role=='manager', User.role=='admin')).all()
    manager_emails = [manager.email for manager in managers]
    return manager_emails


@app.route('/api/generate_monthly_report', methods=['GET'])
# @jwt_required()
# @role_required(roles=['manager', 'admin'])
def generate_monthly_report():
    file_path = generate_pdf_report()

    if os.path.exists(file_path):
        return send_file(
            file_path,
            mimetype='application/pdf',
            download_name="monthly_report.pdf",
            as_attachment=True
        )
    else:
        return "Error: Report not generated.", 500


def calculate_product_score(reviews, ratings):
    sentiment_score = sum(
        TextBlob(review).sentiment.polarity for review in reviews) / len(reviews)
    rating_score = sum(ratings) / len(ratings)
    return round(((0.25 * sentiment_score) + (0.75 * rating_score)), 2)


@app.route('/api/update_product_scores')
def update_product_scores():
    products = Product.query.all()
    for product in products:
        ratings = Rating.query.filter_by(product_id=product.product_id).all()
        if ratings:
            reviews = [rating.review for rating in ratings if rating.review]
            rating_scores = [
                rating.rating for rating in ratings if rating.rating]
            if reviews and rating_scores:
                product.avg_review = calculate_product_score(
                    reviews, rating_scores)
            else:
                product.avg_review = np.nan
        else:
            product.avg_review = np.nan
    db.session.commit()
    return jsonify({'message': 'Product scores updated successfully'}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)
