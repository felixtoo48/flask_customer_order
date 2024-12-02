from flask import Flask, request, jsonify
import mysql.connector
import os
from dotenv import load_dotenv


# load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


# Database connection
db = mysql.connector.connect(
    host="localhost",
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
)


# Models
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)


# creating routes to input/upload customers and orders
@app.route('/customers', methods=['POST'])
def add_customer():
    """ function for adding customers """
    data = request.json
    customer = Customer(name=data['name'], code=data['code'], phone_number=data['phone_number'])
    # db.session.add(customer)
    # db.session.commit()
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
    # db.session.add(order)
    # db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)
