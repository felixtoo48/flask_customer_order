# Savannah Informatics Back End Dev - Technical Challenge

## About The Project
The project is a simple customer order technical challenge question, integrating SMS alerting as well as authorization and authentication using OpenID Connect(AUTH0).

The technical interview was built around a coding assignment that is designed to screen for the following basic skills:
* Experience in developing REST and GraphQL APIs in Python/Go
* Experience with a configuration management tool e.g. Chef, Puppet, Ansible etc
* Experience working with an infrastructure as code tool e.g. Terraform or Pulumi
will be an advantage.
* Experience working with containers and container orchestration tools e.g. k8s
* Experience writing automated tests at all levels - unit, integration and acceptance testing
* Experience with CI/CD (any CI/CD platform)

Particularly the areas of interest include:
* Testing + coverage + CI/CD
* HTTP and APIs e.g. REST
* OAuth2
* Web security e.g. XSS
* Logic / flow of thought
* Setting up a database
* Version control

## Screening Test
1. Create a simple Python or Go service.
2. Design a simple customers and orders database (keep it simple)
3. Add a REST or GraphQL API to input / upload customers and orders:
    - Customers have simple details e.g., name and code.
    - Orders have simple details e.g., item, amount, and time.
4. Implement authentication and authorization via OpenID Connect
5. When an order is added, send the customer an SMS alerting them (you can use the
Africa’s Talking SMS gateway and sandbox)
6. Write unit tests (with coverage checking) and set up CI + automated CD. You can deploy
to any PAAS/FAAS/IAAS of your choice
7. Write a README for the project and host it on your GitHub

## Getting Started

For the technical challenge, I decided to develop the project using Flask because of its simplicity and flexibility, since the the project does not have alot of requirements and MySQL as my database for the project.

#### Functionalities of the project:
* Creating a customer
* Creating an order
* Storing the created orders and customers
* Authentication and Authorization via OpenID Connect
* SMS Alerting using Africa's Talking SMS gateway and sandbox

## Table of Content
* [About The Project](#about-the-project)
* [Screening Test](#screening-test)
* [Getting Started](#getting-started)
* [Environment](#environment)
* [Installation](#installation)
* [Step By Step Guide](#step-by-step-guide)
* [File Descriptions](#file-descriptions)
* [Usage](#usage)
* [Testing](#testing)
* [Bugs](#bugs)
* [Author](#author)
* [License](#license)

## Environment
This project is interpreted/tested on Ubuntu 20.04 LTS using Flask (version 3.0.3)

I created .env file and add the following contents serving as credentials.

```
# yoursecret key
SECRET_KEY=" "

# Database configurations
DB_USERNAME="flask_user"
DB_PASSWORD=" "
DB_HOST="localhost"
DB_NAME="customer_order"

# oidc Auth0 credentials
AUTH0_CLIENT_ID="leAT0LwGQ8bY8fCT8Qj81HYTQcUEanwA"
AUTH0_CLIENT_SECRET=" "
AUTH0_DOMAIN="dev-7fg7hphj1ldi61w0.us.auth0.com"
AUTH0_CALLBACK_URL="http://localhost:5000/callback"

# Africa's talking portal credentials
AT_USERNAME="sandbox"
AT_API_KEY=" "
``` 
You can use your values according to your preference

## Installation
* To get started, install python3 development tools on your virtual machine or virtual environment.
* `sudo apt-get update`
* `sudo apt install mysql-server`
* Setup mysql database: `mysql -u root -p` 
* Create database, create user and grant all priviledges, flush privileges)
* mysql> `CREATE DATABASE customer_order;`
* mysql> `CREATE USER 'flask_user'@'localhost' IDENTIFIED BY 'password';`
* mysql> `GRANT ALL PRIVILEGES ON customer_order.* TO 'flask_user'@'localhost';`
* mysql> `FLUSH PRIVILEGES`
* Install virtual environment
* `sudo -H pip3 install --upgrade pip` then `sudo -H pip3 install virtualenv`
* Create directory and install flask 
* `mkdir flask_customer_order  && cd flask_customer_order`
* Create the project's virtual environment and start it
* `python -m venv venv`
* `source venv/bin/activate`
* `pip install flask mysql-connector-python gunicorn`
* Project structure:
```
flask_customer_order/
│── app.py
│── requirements.txt
│── .env
│── Procfile
|── .github/
|   └── workflows/
|       └── ci_cd.yml
|__ tests/test_app.py
```
* Install packages required
* Or install dependancies from requirements.txt file `pip install -r requirements.txt`
* Create a new flask project `app.py`
* Run app: `flask run`
* Continue development

## Step By Step Guide
1. Setup MySQL database
	- Install MySQL if not already
	- Create database and user
   ### Database Design
       Customer Table: `id`, `name`, `code`, `phone_number`.
       Order Table: `id`, `customer_id`(FK), `item`, `amount`, `time`. 

2. Setup the Flask project following the project structure
3. Coding the flask app
4. Setup environment variables
	- create .env file
5. Configure OIDC with Auth0
	- Sign up and create new application on Auth0
	- Configure:
		* Allowed Login URLs: `http://localhost:5000/loin`
		* Allowed Callback URLs: `http://localhost:5000/callback`
		* Allowed Protected URLs: `http://localhost:5000/protected`
		* Allowed Logout URLs: `http://localhost:5000/logout`
		* Allowed Web Origins URL: `http://localhost:5000`
6. Configure Africa's Talking for SMS integration
	- Sign up
	- Get API key and Username
7. Create tests in `tests/` folder, using pytest
	### Testing Methods
	- Testing using CURL
	or
	- Tests are done using: `pytest`
	or
	- Tests can also be done using coverage: `pytest --cov=app`
8. Set up CI/CD with GitHub Actions

## File Descriptions
[app.py](app.py) - This are the base models or entry point to the project.
#### models - included are the base classes used for this project
Classes in the model:
#### `Customer` - This is the class containing the customers information
* Basic Fields defined
	* `id` - Primary key
 	* `code` - Unique code for every customer
	* `name` - Customer name
	* `phone_number` - customer phone number
* `def before_insert(mapper, connection, target)` - Static method ensuring code is generated if not set manually

#### `Order` - This is the class containing the order information
* Basic fields, utility fields and related field(client foreign key)
	* `id` - Primary key
	* `customer_id` - Foreign key
	* `item` - Ordered item
	* `amount` - Amount of the item

#### Routes - Routes used by the APIs and Auth0
Such routes used include:

#### `/login` - Auth0 login route
* Returns redirect to callback url

#### `/callback` - Callback after login to Auth0
* Returns user information in JSON format

#### `/protected` - Routing for protected view
* Protected user session after login

#### `/logout` - Logout routing from Auth0
* Redirects to login page after seccessfully logging out

#### `/add_customer` - API for creating a customer
* Function for creating/adding a customer or customers

#### `/add_order` - app route for inputting orders and sending SMS alert at the same time
* Function creates new customer orders for valid customers
* Also function sends SMS alert to customer after successfully creating an order through Africa's Talking SMS sandbox gateway

#### Others - Setups and Configurations
Configurations and Setups useful in the flask application for good functionality

#### `Configurations` - File [.env](.env) 
* Database Configuration - MySQL Config data
* Auth0 Configuration
* Flask environment Config key
* Africa's Talking Setup
	* API key = ""
	* Username = Sandbox

#### `def generate_customer_code()` - Function for generating unique customer code
* Generates unique customer code

#### `def requires_auth(f)` - Decorator function for authentication
* Decorator function used in authentication

[.env](.env) - File contains environment variables that are secretive in nature
* File contains environment variables/app credentials i.e. database

[requirements.txt](requirements.txt) - contains project requirements/dependacies


[ci-cd.yml](.github/workflows/ci-cd.yml) - CI/CD Pipeline with GitHub actions
* CI - CD Pipeline with github actions for continuous integration and continuous delivery

[test_app.py](tests/test_app.py) - Test cases for the flask app
#### Tests - Tests written for the app functions
Classes in the model:
#### `TestAPI` - This is the class containing the test cases for app.py
* `def setUp(self)` - Creates test client
* `def tearDown(self)` - Cleans up database after each test
* `def test_login_redirect(self)` - Tests login redirect to Auth0
* `def test_protected_route_without_login(self)` - Tests protected route before login 
* `def test_callback(self, mock_parse_id_token, mock_authorize_access_token)` - Tests call back after login, while on session
* `def test_add_customer(self)` - Tests customer creation
* `def test_add_order(self)` - Tests order creation
* `def test_sms_sending_on_order(self)` - Tests SMS alert after order creation
* `def test_add_customer_invalid(self)` - Tests addition of customer with missing data
* `def test_add_order_invalid_customer(self)` - Tests addition of order for a non existent customer

## Testing
* Testing methods can be conducted as follows:
* Testing can be conducted using CURL

* Testing APIs using CURL example:
  Testing customer API
  ```
  curl -X POST http://localhost:5000/customers \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "phone_number": "+254701234567"}'
  ```
  Testing order API
  ```
  curl -X POST http://localhost:5000/orders \
  -H "Content-Type: application/json" \
  -d '{"customer_id": 1, "item": "Product A", "amount": 150.75}'
  ```
  Testing Incomplete customer data
  ```
  curl -X POST http://localhost:5000/customers \
  -H "Content-Type: application/json" \
  -d '{"name": "Incomplete Customer"}'

  ```
	or
* Tests are done using: `pytest`
        or
* Tests can also be done using coverage: `pytest --cov=app`

## Bugs
1. Auth0 Callback Allowed URL state mismatch between request and response 

## Author
* Felix Too - [Github](https://github.com/felixtoo48) 

## License

MIT License

`Copyright (c) 2024` `Too Felix`

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
