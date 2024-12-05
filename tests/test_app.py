import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
import json
from app import app, db, Customer, Order
import pytest
from unittest.mock import patch


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()  # Creating a test client
        app.config['TESTING'] = True  # Using testing config
        with app.app_context():
            db.create_all()  # Creating test tables

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()  # Cleans up the database after each test

    def test_login_redirect(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 302) # Redirects to Auth0


    def test_protected_route_without_login(self):
        response = self.app.get('/protected')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.headers['Location'])


    @patch('app.auth0.authorize_access_token')
    @patch('app.auth0.parse_id_token')
    def test_callback(self, mock_parse_id_token, mock_authorize_access_token):
        mock_authorize_access_token.return_value = {'id_token': 'test_token'}
        mock_parse_id_token.return_value = {'sub': 'user123', 'email': 'test@example.com'}

        with self.app.session_transaction() as sess:
            sess['nonce'] = 'test_nonce'

        response = self.app.get('/callback')
        self.assertEqual(response.status_code, 200)
        self.assertIn('test@example.com', response.json['email'])



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
            customer = Customer(name="Test Customer", phone_number="+254700000000")
            db.session.add(customer)
            db.session.commit()

            customer_id = customer.id

        response = self.app.post('/orders', json={
            'customer_id': customer_id,
            'item': 'Product Test',
            'amount': 150.75
        })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Order added', data['message'])

    def test_sms_sending_on_order(self):
        with app.app_context():  # Ensure you're inside the app context
            # Create a customer
            customer = Customer(name="Test Customer", phone_number="+254700000000")
            db.session.add(customer)
            db.session.commit()

            customer_id = customer.id

            # Create an order for the customer
            response = self.app.post('/orders', json={
                'customer_id': customer_id,
                'item': 'Product Test',
                'amount': 150.75
            })
        
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 201)
            self.assertIn('Order added', data['message'])


    def test_add_customer_invalid(self):
        # Missing customer data/empty JSON body
        response = self.app.post('/customers', json={})
        self.assertEqual(response.status_code, 400)  # Should fail due to missing data
        data = json.loads(response.data)
        self.assertIn('Missing required fields', data['error'])

        # Test with incomplete fields (missing phone number)
        response = self.app.post('/customers', json={'name': 'John Doe'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('Missing required fields', data['error'])


    def test_add_order_invalid_customer(self):
        # Attempt to add an order for a non-existent customer
        response = self.app.post('/orders', json={
            'customer_id': 9999,  # Non-existent customer ID
            'item': 'Invalid Order',
            'amount': 100
        })
        self.assertEqual(response.status_code, 400)  # Should fail with a bad request error
        data = json.loads(response.data)
        self.assertIn('Customer does not exist', data['error'])


if __name__ == '__main__':
    unittest.main()
