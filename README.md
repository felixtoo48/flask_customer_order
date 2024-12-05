# Savannah Informatics Back End Dev - Technical Challenge
The project is a simple customer order technical challenge question, integrating SMS alerting as well as authorization and authentication using OpenID Connect(AUTH0).

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

They were particularly interested in:
- Testing + coverage + CI/CD
- HTTP and APIs e.g. REST
- OAuth2
- Web security e.g. XSS
- Logic / flow of thought
- Setting up a database
- Version control


## Screening Test

They were particularly interested in:
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
* [Environment](#environment)
* [Installation](#installation)
* [File Descriptions](#file-descriptions)
* [Usage](#usage)
* [Bugs](#bugs)
* [Authors](#authors)
* [License](#license)

## Environment
This project is interpreted/tested on Ubuntu 20.04 LTS using Flask (version 3.0.3)

## Installation
* To get started, install python3 development tools on your virtual machine.
* `sudo apt-get update`
* `sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib`
* Setup postgre database: `sudo -u postgres psql` (Create database, create user and grant all priviledges, alter encoding and timezone role)
* Install virtual environment and install django
* `sudo -H pip3 install --upgrade pip` then `sudo -H pip3 install virtualenv`
* Create directory and install django 
* `mkdir project_portfolio && cd project_portfolio`
* `virtualenv bitinvoiceenv`
* `source bitinvoiceenv/bin/activate`
* Install packages: `pip install django` and `pip install psycopg2`
* Create a new django project called bitinvoice: `django-admin startproject bitinvoice`
* `cd bitinvoice` and edit settings file with Database details
* Run django app: `python manage.py makemigrations` then `python manage.py migrate`
* Create a superuser: `python manage.py createsuperuser`
* Collect static: `python manage.py collectstatic`
* Run app: `python manage.py runserver 0.0.0.0:5000`
* Start the app bitinvoice: `python manage.py startapp bitinvoice_01`

## File Descriptions
[models.py](bitinvoice_01/models.py) - This are the base models for my project, the entry point to the project.
#### models - contains base classes used for this project
Classes in the model:
#### `Client` - This is the class containing the clients information
* Basic Fields and Utility fields defined
* `def __str__(self)` - String representation of the client name, provice and uniqueId
* `def get_absolute_url(self)` - get url of client detail, slug
* `def save(self, *args, **kwargs)` - Autosave function definition

#### `Invoice` - This is the class containing the Invoice inormation
* Basic fields, utility fields and related field(client foreign key)
* `def __str__(self)` - String representation of the number and uniqueId
* `def get_absolute_url(self)` - get url of slug
* `def save(self, *args, **kwargs)` - Autosave function definition

#### `Product` - This is the class containing the products and services information
* Basic fields, utility fields and related field(client foreign key)
* `def __str__(self)` - String representation of the product title and uniqueId
* `def get_absolute_url(self)` - get url of slug
* `def save(self, *args, **kwargs)` - Autosave function definition

#### `Settings` - This is the class containg the settings about the company
* Basic fields, utility fields
* `def __str__(self)` - String representation of the client name, provice and uniqueId
* `def get_absolute_url(self)` - get url of client detail, slug
* `def save(self, *args, **kwargs)` - Autosave function definition


[functions.py](bitinvoice_01/functions.py) - Function definition for emailing invoice to the client
* `def emailInvoiceClient(to_email, from_client, filepath)` - For emailing invoice function

[forms.py](bitinvoice_01/forms.py) - Control form for information input from the front-end view
#### forms - contains classes used for controlling form input
#### `DateInput(forms.DateInput)` - Used to input date
#### `UserLoginForm(forms.ModelForm)` - Class for user log in at the login page
#### `ClientForm(forms.ModelForm)` - Class for client input form
#### `ProductForm(forms.ModelForm)` - Class for product input form
#### `InvoiceForm(forms.ModelForm)` - Invoice details input form
* `def __init__(self, *args, **kwargs)` - Initializing base model
#### `SettingsForm(forms.ModelForm)` - Company settings details input form
#### `ClientSelectForm(forms.ModelForm)` - Client selection form
* `def clean_client(self)` - client removal from the form

[urls.py](bitinvoice_01/urls.py) - Contails urls for respective paths

[views.py](bitinvoice_01/views.py) - Definition of the views rendered
#### views - views rendered/requested
* `def anonymous_required(function=None, redirect_url=None)` - Definition for checking if one is logged in or not to be able to access dashboard, and invoice
* `def login(request)` - Log in request
* `def dashboard(request)` - Dashboard request definition
* `def index(request)` - landing page request definition


## Bugs
No known bugs at this time. 

## Authors
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
