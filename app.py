from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from datetime import datetime
import uuid
import random


# load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flask_user:PasswordHere1234.@localhost/customer_order'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


def generate_customer_code():
    return f"CUST{random.randint(10000, 99999)}"  # generates CUST followed by 5 digits


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


# creating routes to input/upload customers and orders
@app.route('/customers', methods=['POST'])
def add_customer():
    """ function for adding customers """
    data = request.json
    customer = Customer(name=data['name'], code=data['code'], phone_number=data['phone_number'])
    db.session.add(customer)
    db.session.commit()
    return jsonify({'message': 'Customer added', 'id': customer.id}), 201


@app.route('/orders', methods=['POST'])
def add_order():
    """ function for adding orders """
    data = request.json
    order = Order(
        customer_id=data['customer_id'],
        item=data['item'],
        amount=data['amount'],
        time=data['time']
    )
    db.session.add(order)
    db.session.commit()

    # Send SMS to the customer
    customer = Customer.query.get(data['customer_id'])
    if customer:
        message = (
            f"Order placed: {data['item']} for ${data['amount']}. "
            "This message was sent using the Africa's Talking SMS gateway and sandbox."
        )
        sms.send(message, [customer.phone_number])

    return jsonify({'message': 'Order added', 'order_id': order.id}), 201


if __name__ == '__main__':
    app.run(debug=True)
