from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy


# load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flask_user:Password@1234@localhost/customer_order'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


# Models
class Customer(db.Model):
    """ customers model crestion """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)


class Order(db.Model):
    """ orders model creation """
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    item = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    time = db.Column(db.DateTime, nullable=False)


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


if __name__ == '__main__':
    app.run(debug=True)
