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
@role_required(roles=['manager', 'admin'])
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
        cart = Cart.query.filter_by(
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

        # Save items in the order and update product quantities
        for item in cart_items:
            product = Product.query.get(item['id'])

            if product:
                # Check if the product has enough quantity in stock
                if product.stock < item['qty']:
                    return jsonify({'message': 'Not enough quantity in stock for product {}'.format(product.product_name)}), 400

                # Create order item
                order_item = OrderItem(
                    order_id=order.order_id,
                    product_id=product.product_id,
                    category_id=product.category_id,
                    quantity=item['qty'],
                    total_price=item['price'] * item['qty']
                )
                db.session.add(order_item)

                # Update product quantity in the database
                product.stock -= item['qty']

        db.session.commit()

        return jsonify({'message': 'Checkout successful'}), 200

    except Exception as e:
        print(f"Error during checkout: {str(e)}")
        db.session.rollback()  # Rollback changes in case of an error
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
        categories = Category.query.filter_by(category_approval=1).all()
        category_list = []

        for category in categories:
            category_data = {
                'category_id': category.category_id,
                'name': category.category_name,
                'image': category.category_image
            }
            category_list.append(category_data)

        return jsonify({'categories': category_list}), 200
    except Exception as e:
        return jsonify({'message': 'Error fetching categories', 'error': str(e)}), 500


# Add Category
@app.route('/api/add_category', methods=['POST'])
@jwt_required()
@role_required(roles=['admin'])
def add_category():

    name = request.json['name']
    image = request.json['image']

    if request.json['image'] == '':
        image = 'https://maxicus.com/wp-content/uploads/2022/05/Virtual-Shopping-A-Step-into-the-Future-of-Retail.png'
    else:
        image = request.json['image']

    category = Category(category_name=name, category_image=image)

    try:
        db.session.add(category)
        db.session.commit()

        return jsonify({'message': 'Category Added Successfully!'}), 200

    except Exception as e:
        return jsonify({'message': 'Error Adding the Category', 'error': str(e)}), 500


# Update Database Record in Category
@app.route('/api/edit_category/<int:category_id>', methods=['PUT'])
@jwt_required()
@role_required(roles=['admin'])
def update_category(category_id):
    category_to_update = Category.query.get_or_404(category_id)
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
        return jsonify({'message': 'Error Updating the Category', 'error': str(e)}), 500


# Delete a Category from the Database Record
@app.route('/delete_category/<int:category_id>', methods=['DELETE'])
@jwt_required()
@role_required(roles=['admin'])
def delete_category(category_id):
    category_to_delete = Category.query.get_or_404(category_id)

    try:
        db.session.delete(category_to_delete)
        db.session.commit()
        return jsonify({'message': "Category Deleted Successfully!"}), 200

    except Exception as e:
        return jsonify({'message': 'Error deleting the category', 'error': str(e)}), 500


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


# Add a Product to the Database
@app.route('/api/<int:category_id>/add_product', methods=['POST'])
@jwt_required()
@role_required(roles=['admin', 'manager'])
def add_product(category_id):

    name = request.json['name']
    # image = request.json['image']
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
@app.route('/api/edit_product/<int:product_id>', methods=['PUT'])
@jwt_required()
@role_required(roles=['admin', 'manager'])
def update_product(product_id):

    product_to_update = Product.query.get_or_404(product_id)
    data = request.json

    try:
        product_to_update.product_name = data['name']
        # product_to_update.product_image = data['image']
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
@app.route('/delete_product/<int:product_id>', methods=['DELETE'])
@jwt_required()
@role_required(roles=['admin', 'manager'])
def delete_product(product_id):
    product_to_delete = Product.query.get(product_id)
    if not product_to_delete:
        return jsonify({'message': 'Product not found'}), 404

    try:
        db.session.delete(product_to_delete)
        db.session.commit()
        return jsonify({'message': "Product Deleted Successfully!"}), 200

    except Exception as e:
        return jsonify({'message': 'Error deleting the product', 'error': str(e)}), 500


# Show the Categories and Products on the Manager & Admin Dashboard
@app.route('/api/manager_admin_dashboard', methods=['GET'])
@jwt_required()
@role_required(roles=['manager', 'admin'])
def manager_admin_dashboard():
    try:
        categories = Category.query.order_by(Category.category_id).all()

        # Create a dictionary to store products per category
        products_by_category = {}

        # Fetch products for each category and store them in the dictionary
        for category in categories:
            products = Product.query.filter_by(
                category_id=category.category_id).all()

            # Convert Product objects to dictionaries
            products_data = []
            for product in products:
                products_data.append({
                    'name': product.product_name,
                    'image': product.product_image,
                    'manufacture_date': product.manufacturing_date,
                    'price': product.price,
                    'unit': product.unit,
                    'stock': product.stock,
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
@role_required(roles=['admin'])
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
@role_required(roles=['admin'])
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


# Approve manager request
@app.route('/admin/approve/<int:user_id>', methods=['PUT'])
@jwt_required()
@role_required(roles=['admin'])
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


# Decline manager request
@app.route('/admin/decline/<int:user_id>', methods=['PUT'])
@jwt_required()
@role_required(roles=['admin'])
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


# Revert manager status
@app.route('/admin/revert/<int:user_id>', methods=['PUT'])
@jwt_required()
@role_required(roles=['admin'])
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


# Fetch pending categories
@app.route('/admin/pending_categories', methods=['GET'])
@jwt_required()
@role_required(roles=['admin'])
def get_pending_categories():
    try:
        # Fetch a list of pending category requests from the database
        pending_categories = Category.query.filter_by(
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
        # Update the request_approval status to 1 for the specified category
        category = Category.query.get(category_id)
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
        # Update the request_approval status to -1 for the specified category
        category = Category.query.get(category_id)
        if category:
            category.category_approval = -1
            db.session.commit()
            return jsonify({'message': 'Category request declined'}), 200
        else:
            return jsonify({'message': 'Category not found'}), 404
    except Exception as e:
        return jsonify({'message': 'Error declining request', 'error': str(e)}), 500


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
