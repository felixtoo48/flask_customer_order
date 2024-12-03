import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
import json
from app import app, db, Customer, Order  # Import your Flask app and models


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()  # Create a test client
        app.config['TESTING'] = True  # Use testing config
        with app.app_context():
            db.create_all()  # Create test tables

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()  # Clean up the database after each test

    def test_add_customer(self):
        response = self.app.post('/customers', json={
            'name': 'John Doe',
            'phone_number': '+254701234567'
        })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Customer added', data['message'])

    def test_add_order(self):
        with app.app_context():
            customer = Customer(name="Jane Doe", phone_number="+254700000000")
            db.session.add(customer)
            db.session.commit()

        response = self.app.post('/orders', json={
            'customer_id': 1,
            'item': 'Product A',
            'amount': 150.75
        })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Order added', data['message'])

if __name__ == '__main__':
    unittest.main()

