from flask import Flask, request, jsonify, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from datetime import datetime
import random
from flask_oidc import OpenIDConnect
import africastalking
from functools import wraps
from authlib.common.security import generate_token


# load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flask_user:PasswordHere1234.@localhost/customer_order'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False


db = SQLAlchemy(app)


# Configure Auth0
oauth = OAuth(app)
auth0 = oauth.register(
    'auth0',
    client_id=os.getenv('AUTH0_CLIENT_ID'),
    client_secret=os.getenv('AUTH0_CLIENT_SECRET'),
    api_base_url=f'https://{os.getenv("AUTH0_DOMAIN")}',
    access_token_url=f'https://{os.getenv("AUTH0_DOMAIN")}/oauth/token',
    authorize_url=f'https://{os.getenv("AUTH0_DOMAIN")}/authorize',
    server_metadata_url=f'https://{os.getenv("AUTH0_DOMAIN")}/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid profile email',
    }
)

# Africa's Talking setup
africastalking.initialize(
    username=os.getenv('AT_USERNAME'),
    api_key=os.getenv('AT_API_KEY')
)
sms = africastalking.SMS


def generate_customer_code():
    """ function for generating unique code for customer """
    return f"CUST{random.randint(10000, 99999)}"


# Models
class Customer(db.Model):
    """ customers model crestion """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False, default=generate_customer_code)
    phone_number = db.Column(db.String(20), nullable=False)

    # Ensure 'code' is generated if not set manually:
    @staticmethod
    def before_insert(mapper, connection, target):
        if not target.code:
            target.code = generate_customer_code()


# Register the event to trigger before an insert operation
event.listen(Customer, 'before_insert', Customer.before_insert)


class Order(db.Model):
    """ orders model creation """
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    item = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.now)


# Auth0 routes
@app.route('/login')
def login():
    """ Auth0 login function"""

    # Generate a secure random nonce and store it in the session
    nonce = generate_token()  
    session['nonce'] = nonce

    # Generate a random state for CSRF protection and store it in the session
    state = generate_token()  
    session['state'] = state

    # Redirect to Auth0 with the nonce and state
    return auth0.authorize_redirect(redirect_uri=os.getenv('AUTH0_CALLBACK_URL'), nonce=nonce, state=state)

@app.route('/callback')
def callback():
    """ call back after login """
    # Retrieve and validate the nonce from the session
    nonce = session.pop('nonce', None)

    token = auth0.authorize_access_token()  # Retrieves the token from Auth0
    print("Access Token:", token)  # Print the full token for debugging

    user_info = auth0.parse_id_token(token, nonce=nonce)
    session['user'] = user_info  # Save user info in session
    return jsonify(user_info)

@app.route('/protected')
def protected():
    """ protected user session after login """
    print("Session data:", session.get('user'))  # Check if the user is logged in
    if not session.get('user'):
        return redirect('/login')  # Redirect if no user session
    return jsonify({"message": "User is logged in"})  

@app.route('/logout')
def logout():
    """ logout function """
    session.clear()
    return redirect(
    f'https://{os.getenv("AUTH0_DOMAIN")}/v2/logout?'
    f'returnTo={url_for("login", _external=True)}'
    f'&client_id={os.getenv("AUTH0_CLIENT_ID")}'
)

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

# creating routes to input/upload customers and orders
@app.route('/customers', methods=['POST'])
# @requires_auth
def add_customer():
    """ function for adding customers """
    data = request.json

    customer = Customer(name=data['name'], phone_number=data['phone_number'])

    db.session.add(customer)
    db.session.commit()

    return jsonify({'message': 'Customer added', 'id': customer.id, 'code': customer.code}), 201

@app.route('/orders', methods=['POST'])
# @requires_auth
def add_order():
    """ function for adding orders """
    data = request.json
    order = Order(
        customer_id=data['customer_id'],
        item=data['item'],
        amount=data['amount']
    )
    db.session.add(order)
    db.session.commit()

    # Send SMS to the customer
    customer = db.session.get(Customer, data['customer_id'])
    if customer:
        message = (
            f"Order placed: {data['item']} for ${data['amount']}. "
            "This message was sent using the Africa's Talking SMS gateway and sandbox."
        )

        try:
            response = sms.send(message, [customer.phone_number], sender_id='20267')
            print(response)
        except Exception as e:
            print(f"Error sending SMS: {e}")


    return jsonify({'message': 'Order added', 'order_id': order.id}), 201


if __name__ == '__main__':
    app.run(debug=True)
