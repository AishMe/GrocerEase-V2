from models import User, Cart, Order, OrderItem, Product, Category, db, bcrypt, ma
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask import Flask, jsonify, request, send_file
from tasks import export_product_data_to_csv
from functools import wraps
from flask_cors import CORS
from datetime import date
import os

basedir = os.path.abspath(os.path.dirname(__file__))
# print("BASE DIR PATH: ", basedir)

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


# Example of using the decorator to protect an endpoint
@app.route('/api/manager', methods=['GET'])
@jwt_required()
@role_required(roles=['manager'])
def admin_endpoint():
    # This endpoint can only be accessed by users with the 'admin' role
    return jsonify({'message': 'You have access to the admin endpoint.'})


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

@app.route('/api/add_to_cart', methods=['POST'])
@jwt_required()
def add_to_cart():
    try:
        data = request.json
        product_id = data.get('product_id')
        quantity = data.get('quantity')
        user_id = get_jwt_identity().get('userId')

        # Check if the product exists
        product = Product.query.filter_by(product_id=product_id).all
        if not product:
            return jsonify({'message': 'Product not found'}), 404

        # Check if the user has an active cart or create a new one
        cart = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
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
        print(e)
        return jsonify({'message': 'Failed to add to cart'}), 500


# New Flask route for checkout
@app.route('/api/checkout', methods=['POST'])
@jwt_required()
@role_required(roles=['user'])
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
@role_required(roles=['user'])
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


# @app.route('/api/products', methods=['GET'])
# def get_products():
#     try:
#         products = Product.query.all()
#         product_list = []

#         for product in products:
#             product_data = {
#                 'id': product.product_id,
#                 'category_id': product.category_id,
#                 'name': product.product_name,
#                 'description': product.description,
#                 'price': product.price,
#                 'image': product.product_image
#             }
#             product_list.append(product_data)

#         return jsonify({'products': product_list}), 200
#     except Exception as e:
#         return jsonify({'message': 'Error fetching products', 'error': str(e)}), 500



@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        category_id = request.args.get('category_id')
        if category_id:
            # Filter products by category_id
            products = Product.query.filter_by(category_id=category_id).all()
        else:
            # Fetch all products
            products = Product.query.all()

        product_list = []

        for product in products:
            product_data = {
                'id': product.product_id,
                'category_id': product.category_id,
                'name': product.product_name,
                'description': product.description,
                'manufacturing_date': product.manufacturing_date,
                'stock': product.stock,
                'unit': product.unit,
                'price': product.price,
                'image': product.product_image
            }
            product_list.append(product_data)

        return jsonify({'products': product_list}), 200
    except Exception as e:
        return jsonify({'message': 'Error fetching products', 'error': str(e)}), 500



# Fetch pending managers
@app.route('/admin/pending/managers', methods=['GET'])
@jwt_required()
def get_pending_managers():
    try:
        # Fetch a list of pending manager requests from the database
        pending_managers = User.query.filter_by(request_approval=0).all()
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
def get_approved_managers():
    try:
        # Fetch a list of pending manager requests from the database
        pending_managers = User.query.filter_by(request_approval=1).all()
        pending_managers_data = [{'user_id': manager.user_id,
                                  'name': manager.name,
                                  'role': manager.role,
                                  'avatar': manager.avatar,
                                  'email': manager.email
                                  } for manager in pending_managers]

        return jsonify({'approvedManagers': pending_managers_data}), 200
    except Exception as e:
        return jsonify({'message': 'Error fetching pending managers', 'error': str(e)}), 500


# Fetch rejected managers
@app.route('/admin/rejected/managers', methods=['GET'])
@jwt_required()
def get_rejected_managers():
    try:
        # Fetch a list of pending manager requests from the database
        pending_managers = User.query.filter_by(request_approval=-1).all()
        pending_managers_data = [{'user_id': manager.user_id,
                                  'name': manager.name,
                                  'role': manager.role,
                                  'avatar': manager.avatar,
                                  'email': manager.email
                                  } for manager in pending_managers]

        return jsonify({'rejectedManagers': pending_managers_data}), 200
    except Exception as e:
        return jsonify({'message': 'Error fetching pending managers', 'error': str(e)}), 500


# Approve request
@app.route('/admin/approve/<int:user_id>', methods=['PUT'])
@jwt_required()
def approve_request(user_id):
    try:
        # Update the request_approval status to 1 for the specified user
        user = User.query.get(user_id)
        if user:
            user.request_approval = 1
            db.session.commit()
            return jsonify({'message': 'Request approved'}), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'message': 'Error approving request', 'error': str(e)}), 500

# Decline request


@app.route('/admin/decline/<int:user_id>', methods=['PUT'])
@jwt_required()
def decline_request(user_id):
    try:
        # Update the request_approval status to -1 for the specified user
        user = User.query.get(user_id)
        if user:
            user.request_approval = -1
            db.session.commit()
            return jsonify({'message': 'Request declined'}), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'message': 'Error declining request', 'error': str(e)}), 500


# Decline request
@app.route('/admin/revert/<int:user_id>', methods=['PUT'])
@jwt_required()
def revert_request(user_id):
    try:
        # Update the request_approval status to -1 for the specified user
        user = User.query.get(user_id)
        if user:
            user.request_approval = 0
            db.session.commit()
            return jsonify({'message': 'Action Performed Successfully'}), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'message': 'Error processing request', 'error': str(e)}), 500


# @app.route('/category/add', methods=['POST'])
# def add_details():
#     email = request.json['email']
#     name = request.json['name']
#     password = request.json['password']
#     role = request.json['role']

#     add_category = Category(category_name=category_name,
#                     category_image=category_image)

#     db.session.add(add_category)
#     db.session.commit()

#     return jsonify({'msg': 'Category Added Successfully!'})


@app.route('/api/visited_status', methods=['GET'])
def user_visited_status():
    try:

        # Get today's date
        today_date = date.today()
        print(date.today())
        print(Order.order_date.cast(db.Date))

        # Query orders with order_date on today's date
        orders_today = Order.query.filter(Order.order_date == today_date).all()
        print(orders_today)
        user_ids_today = set(order.user_id for order in orders_today)

        # Query users who are not in the list of user_ids with orders today
        users = User.query.filter(User.user_id.notin_(
            user_ids_today), User.role == 'user').all()

        # Extract user names from user objects
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



if __name__ == "__main__":
    app.run(debug=True)
