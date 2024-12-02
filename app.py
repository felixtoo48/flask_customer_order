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

if __name__ == '__main__':
    app.run(debug=True)
