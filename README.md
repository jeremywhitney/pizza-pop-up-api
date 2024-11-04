# Pizza Pop-Up API

A Django REST framework-powered backend API for the Pizza Pop-Up restaurant application. This API handles menu management, order processing, and customer interactions.

## Table of Contents
- [System Overview](#system-overview)
- [Data Models](#data-models)
- [Installation](#installation)
- [Getting Started Tutorial](#getting-started-tutorial)

## System Overview

### User Types and Permissions
- **Customers**
  - Can view available products
  - Can create and manage their orders
  - Can view their own profile, payments, and order history
  
- **Staff (Employees)**
  - All customer permissions
  - Can manage products (create, update, delete)
  - Can view and update all orders
  - Can view all customer profiles
  - Have additional profile fields (position, pay rate)

### Order Flow
1. Cart Phase
   - User adds items to cart (stored in session storage)
   - For pizzas, toppings can be added/removed
   - No database record until checkout
   
2. Order Creation
   - User provides payment information
   - Order is created in database with status "PENDING"
   - Payment is associated with order
   
3. Processing
   - Staff can change order status to "IN_PROCESS"
   - Employee is assigned to order when processing begins
   
4. Completion
   - Staff can mark order as "COMPLETED"
   - Completed orders cannot be modified

## Data Models

### User-Related Models
User (Django Default)
- Profile
  - phone_number
  - address
  - EmployeeProfile (if staff)
    - position
    - rate

### Product-Related Models
Category
- Product
  - name
  - price
  - description
  - category (1-5)
  - image_path
  - is_available

Categories:
1. Beverages
2. Pizza
3. Plates
4. Sides
5. Toppings

### Order-Related Models
Order
- customer (Profile)
- employee (Profile)
- payment
- status
- OrderProduct (Line Items)
  - product
  - quantity
  - PizzaTopping (if product is Pizza)
    - topping (Product from category 5)

## Installation

### Prerequisites
- Python 3.12
- Pipenv
- Visual Studio Code

### Setup
1. Clone the repository
git clone https://github.com/jeremywhitney/pizza-pop-up-api.git
cd pizza-pop-up-api

2. Start the virtual environment
pipenv shell

3. Install dependencies
pipenv install

4. Set up the database and migrations
./seed_database.sh

This script will:
- Remove existing database and migrations
- Create new migrations
- Apply migrations in the correct order for all models
- Set up a fresh database ready for use

### Running the Server
1. Open the project in Visual Studio Code
2. Make sure you're in the Pipenv shell
3. Use the 'Python: Django' debugger in VS Code to run the server

### Dependencies
All dependencies are managed through Pipenv:
- django
- djangorestframework
- django-cors-headers
- pillow (for image handling)
- autopep8
- pylint
- pylint-django

## Getting Started Tutorial

Follow this tutorial to see a complete flow from user registration to order processing.

### 1. Register New Customer
POST /register
```json
{
   "username": "johndoe",
   "password": "securepass123",
   "email": "john@example.com",
   "first_name": "John",
   "last_name": "Doe",
   "phone_number": "555-0123",
   "address": "123 Main St"
}
```

Response:
```json
{
   "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
   "user_id": 1,
   "is_staff": false
}
```

### 2. View Profile Information

#### Customer Profile
GET /profile

Response:
```json
{
   "profile": {
       "id": 1,
       "username": "johndoe",
       "first_name": "John",
       "last_name": "Doe",
       "email": "john@example.com",
       "is_staff": false,
       "phone_number": "555-0123",
       "address": "123 Main St"
   },
   "payments": [],
   "orders": []
}
```

#### Employee Profile Example
GET /profile

Response:
```json
{
   "profile": {
       "id": 2,
       "username": "employee1",
       "first_name": "Jane",
       "last_name": "Smith",
       "email": "jane@pizzapopup.com",
       "is_staff": true,
       "phone_number": "555-0124",
       "address": "456 Oak St",
       "position": "Chef",
       "rate": 15.50,
       "date_joined": "11-04-2024"
   }
}
```

### 3. Add Payment Method
POST /payments
```json
{
   "merchant_name": "VISA",
   "account_number": "4111111111111111",
   "expiration_date": "2025-12"
}
```

Response:
```json
{
   "id": 1,
   "merchant_name": "VISA",
   "account_number": "****1111",
   "customer": {
       "id": 1,
       "username": "johndoe",
       "first_name": "John",
       "last_name": "Doe",
       "email": "john@example.com",
       "is_staff": false,
       "phone_number": "555-0123",
       "address": "123 Main St"
   },
   "expiration_date": "2025-12",
   "create_date": "2024-11-04T10:30:00Z"
}
```

### 4. Create New Order
POST /orders
```json
{
   "payment": 1,
   "products": [
       {
           "id": 1,  // Tomato Pie
           "quantity": 1,
           "toppings": [
               {"id": 11}  // Anchovy
           ]
       },
       {
           "id": 5,  // Buffalo Wings
           "quantity": 1
       },
       {
           "id": 17,  // Soda
           "quantity": 1
       }
   ]
}
```

Response:
```json
{
   "id": 1,
   "customer": {
       "id": 1,
       "username": "johndoe"
   },
   "status": "PENDING",
   "created_date": "2024-11-04T10:30:00Z",
   "products": [
       {
           "id": 1,
           "name": "Tomato Pie",
           "price": 14.99,
           "quantity": 1,
           "toppings": [
               {
                   "id": 11,
                   "name": "Anchovy",
                   "price": 1.50
               }
           ]
       },
       {
           "id": 5,
           "name": "Buffalo Wings",
           "price": 12.99,
           "quantity": 1,
           "toppings": []
       },
       {
           "id": 17,
           "name": "Soda",
           "price": 2.49,
           "quantity": 1,
           "toppings": []
       }
   ],
   "payment": {
       "id": 1,
       "merchant_name": "VISA",
       "account_number": "****1111",
       "customer": {
           "id": 1,
           "username": "johndoe"
       },
       "expiration_date": "2025-12"
   },
   "total_price": 31.97
}
```

### 5. Update Order Status (Staff Only)
PATCH /orders/1
```json
{
   "status": "IN_PROCESS"
}
```

Response:
```json
{
   "id": 1,
   "customer": {
       "id": 1,
       "username": "johndoe"
   },
   "status": "IN_PROCESS",
   "created_date": "2024-11-04T10:30:00Z",
   "products": [
       {
           "id": 1,
           "name": "Tomato Pie",
           "price": 14.99,
           "quantity": 1,
           "toppings": [
               {
                   "id": 11,
                   "name": "Anchovy",
                   "price": 1.50
               }
           ]
       },
       {
           "id": 5,
           "name": "Buffalo Wings",
           "price": 12.99,
           "quantity": 1,
           "toppings": []
       },
       {
           "id": 17,
           "name": "Soda",
           "price": 2.49,
           "quantity": 1,
           "toppings": []
       }
   ],
   "employee": {
       "id": 2,
       "username": "employee1"
   },
   "payment": {
       "id": 1,
       "merchant_name": "VISA",
       "account_number": "****1111",
       "customer": {
           "id": 1,
           "username": "johndoe"
       },
       "expiration_date": "2025-12"
   },
   "total_price": 31.97
}
```