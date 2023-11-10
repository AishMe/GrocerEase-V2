from flask import Flask, jsonify, request
from models import User, Order, OrderItem, Product, Category, db, bcrypt, ma
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


# New Flask route for checkout
@app.route('/api/checkout', methods=['POST'])
@jwt_required()
def checkout():
    try:
        user_id = get_jwt_identity()['userId']
        cart_items = request.json.get('cart')

        # Create a new order
        order = Order(user_id=user_id)
        db.session.add(order)
        db.session.commit()

        # Save items in the order
        for item in cart_items:
            product = Product.query.get(item['id'])

            if product:
                order_item = OrderItem(
                    order_id=order.order_id,
                    product_id=product.product_id,
                    category_id=product.category_id,  # Associate category with the product
                    quantity=item['qty'],
                    total_price=item['price'] * item['qty']
                )
                db.session.add(order_item)

        db.session.commit()

        return jsonify({'message': 'Checkout successful'}), 200

    except Exception as e:
        print(f"Error during checkout: {str(e)}")
        return jsonify({'message': 'Error during checkout', 'error': str(e)}), 500


@app.route('/api/orders', methods=['GET'])
@jwt_required()
def get_orders():
    try:
        user_id = get_jwt_identity()['userId']
        orders = Order.query.filter_by(user_id=user_id).order_by(
            Order.order_date.desc()).all()

        formatted_orders = []

        for order in orders:
            order_items = OrderItem.query.filter_by(
                order_id=order.order_id).all()
            order_data = {
                'order_id': order.order_id,
                'order_date': order.order_date,
                'categories': []
            }

            category_dict = {}
            for item in order_items:
                product = Product.query.get(item.product_id)
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


@app.route('/api/categories', methods=['GET'])
def get_categories():
    try:
        categories = Category.query.all()
        category_list = []

        for category in categories:
            category_data = {
                'id': category.category_id,
                'name': category.category_name,
                'image': category.category_image
            }
            category_list.append(category_data)

        return jsonify({'categories': category_list}), 200
    except Exception as e:
        return jsonify({'message': 'Error fetching categories', 'error': str(e)}), 500


@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        products = Product.query.all()
        product_list = []

        for product in products:
            product_data = {
                'id': product.product_id,
                'category_id': product.category_id,
                'name': product.product_name,
                'description': product.description,
                'price': product.price,
                'image': product.product_image
            }
            product_list.append(product_data)

        return jsonify({'products': product_list}), 200
    except Exception as e:
        return jsonify({'message': 'Error fetching products', 'error': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
