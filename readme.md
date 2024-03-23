# Xander Salathe - Coder Academy - T2A2 - API Webserver Project

## Introduction

The Finance Manager API is a backend service designed to empower individuals and small businesses to effectively manage their financial data. It provides a comprehensive suite of features for tracking transactions, managing accounts, and categorizing expenses and income. By offering endpoints for creating, reading, updating, and deleting financial records, it adheres to the RESTful principles, ensuring a scalable, flexible, and intuitive interface for developers and applications.

## System/Hardware Requirements

- No specific hardware requirements.
- Operating System: Compatible with any OS that can run Python 3 (e.g., Windows, macOS, Linux).

## App Setup

All endpoints are documented in this README document, and can be imported from the endpoints.json file to either Insomnia, or Postman.

To run from local machine using postgreSQL:

1. Create a new postgreSQL User and give Permissions
2. Create a postgreSQL Database
3. Edit ".env" file so "SQL_DATABASE_URI" matches user and database details
4. Start python virtual invironment (python3 -m venv venv)
5. Activate virtual environment (source venv/bin/activate)
6. Install requirements (pip3 install -r requirements.txt)
7. Create and seed tables (flask db drop && flask db create && flask db seed)
8. Run flask app (flask run)

## Note for assessors:

For ease of assessment, I have created a postgreSQL Databased hosted via [Neon.tech](neon.tech) - as such no configuration is required on your end to test functionality of this application.

The details for this are saved in the .env file included in submission, however for obvious reasons this is not shared directly to GitHub. As such, the only steps needed to be taken is to create and seed the tables, and run the flask server:

1. `flask db drop && flask db create && flask db seed`

2. `flask run`

## License

Distributed under the terms of the MIT License


## API Endpoint Documentation

<details>
  <summary>Click here for response </summary>

## Account Controller:

<details>
  <summary>Click here for Account Controller Endpoints </summary>

### 1. Create a New Account

### `/accounts - POST`

**This endpoint is protected and requires a valid JWT token.**

#### Description:

Used to create a new Account in relation to a User

#### Required parameters:

- `account_type`: (`str`) type or description of account
- `balance`: (`int`) initial value of account

eg

```json
{
  "account_type": "savings",
  "balance": 15000
}
```

#### Expected response:

JSON response of Account, 201

Example response:

```json
{
  "id": 4,
  "account_type": "test",
  "balance": "15000.00",
  "transactions": [],
  "date_created": "2024-03-22T09:55:02.430673",
  "user": {
    "username": "User",
    "email": "user@email.com"
  }
}
```

### 2. Get a List of All Accounts (with Role-Based Filtering)

### `/accounts - GET`

**This endpoint is protected and requires a valid JWT token.**

#### Description:

Retrieves a list of all accounts. Auditors can see all accounts, while other users see only their own.

#### No parameters required.

#### Expected response:

JSON array of Account objects.

Example response:

```json
[
  {
    "id": 1,
    "account_type": "savings",
    "balance": "1234.56",
    "date_created": "2024-03-20T12:34:56.789Z",
    "user": {
      "username": "Admin",
      "email": "admin@email.com"
    }
  }
]
```


### 3. Get a Specific Account

### `/accounts/<account_id> - GET`

**This endpoint is protected and requires a valid JWT token.**

#### Description:

Retrieves information about a specific account. Auditors can view any account, while other users can only view their own accounts.

#### Required parameters:

- `account_id`: URL parameter specifying the account's ID.

#### Expected response:

JSON representation of the specified Account

Example response:

```json
{
  "id": 2,
  "account_type": "checking",
  "balance": "5000.00",
  "date_created": "2024-03-21T11:22:33.444Z",
  "user": {
    "username": "User",
    "email": "user@email.com"
  }
}
```

### 4. Update an Existing Account

### `/accounts/<account_id> - PUT/PATCH`

**This endpoint is protected and requires a valid JWT token. Only Admins can update accounts not owned by themselves.**

#### Description:

Updates information about a specific account.

#### Required parameters:

- `account_type`: (Optional, `str`) New type or description of the account.
- `balance`: (Optional, `int`) New balance value for the account.

#### Example request:

```json
{
  "account_type": "emergency fund",
  "balance": 20000
}
```

#### Expected response:

JSON representation of the updated Account, 201.

#### Example response:

```json
{
  "id": 2,
  "account_type": "emergency fund",
  "balance": "20000.00",
  "transactions": [],
  "date_created": "2024-03-21T11:22:33.444Z",
  "user": {
    "username": "User",
    "email": "user@email.com"
  }
}
```

### 5. Delete an Existing Account

### `/accounts/<account_id> - DELETE`

**This endpoint is protected and requires a valid JWT token. Only Admins can delete accounts not owned by themselves.**

#### Description:

Deletes a specific account.

#### Required parameters:

- `account_id`: URL parameter specifying the account's ID.

#### Expected response:

Confirmation message of the deleted account, 201

Example response:

```json
{
  "message": "Account 'emergency fund' deleted successfully"
}
```

### 6. Get Total Balance (Auditor Only)

### `/accounts/total_balance - GET`

**This endpoint is protected and requires a valid JWT token. Only accessible by users with the "Auditor" role.**

#### Description:

Calculates the total balance across all accounts in the system.

#### No parameters required.

#### Expected response:

JSON object with the total balance.

Example response:

```json
{
  "total_balance": "27345.01"
}
```


### 7. Rank Transactions within an Account (Auditor Only)

### `/accounts/<int:account_id>/transactions/rank - GET`

**This endpoint is protected and requires a valid JWT token. Only accessible by users with the "Auditor" role.**

#### Description:

Ranks transactions within a specific account based on the amount, showing the relative size of each transaction.

#### Required parameters:

- `account_id`: URL parameter specifying the account's ID to rank transactions within.

#### Expected response:

JSON array of transactions with their ranks.

Example response:

```json
[
  {
    "transaction_id": 3,
    "amount": "-500.00",
    "rank": 1
  },
  {
    "transaction_id": 1,
    "amount": "-300.00",
    "rank": 2
  }
]
```

### 8. Account Summary (Auditor Only)

### `/accounts/summary - GET`

**This endpoint is protected and requires a valid JWT token. Only accessible by users with the "Auditor" role.**

#### Description:

Provides a summary of each account including the account ID, type, and total spent in transactions.

#### No parameters required.

#### Expected response:

JSON array with a summary for each account.

Example response:

```json
[
  {
    "account_id": 1,
    "account_type": "savings",
    "total_spent": "-560.00"
  },
  {
    "account_id": 2,
    "account_type": "checking",
    "total_spent": "-1230.00"
  }
]
```

### 9. Search Transactions (with Role-Based Filtering)

### `/accounts/search - POST`

**This endpoint is protected and requires a valid JWT token. It enables searching for transactions based on a description, with results filtered by the user's role.**

#### Description:

Allows users to search for transactions across all accounts if they have the "Auditor" role. Regular users can only search within their own accounts.

#### Required parameters (in JSON body):

- `query`: (`str`) The search term to filter transactions by their description.

Example request:

```json
{
  "query": "groceries"
}
```

#### Expected response:

JSON array of transactions matching the search term, filtered according to the user's role.

Example response (for an "Auditor"):

```json
[
  {
    "id": 2,
    "amount": "-123.45",
    "description": "groceries at mart",
    "transaction_date": "2024-03-22T09:55:02.430673",
    "account": {
      "id": 1,
      "account_type": "checking"
    }
  }
]
```

</details>

## Auth Controller:

<details>
  <summary>Click here for Auth Controller Endpoints </summary>

### 1. Get All Users (Auditor Only)

### `/auth/users - GET`

**This endpoint is protected and requires a valid JWT token. Only accessible by users with the "Auditor" role.**

#### Description:

Retrieves a list of all registered users in the system.

#### No parameters required.

#### Expected response:

JSON array of User objects, 201

Example response:

```sql
[
    {
        "id": 1,
        "username": "Admin",
        "email": "admin@email.com",
        "role": "Admin",
        "date_created": "2024-03-20T12:00:00Z"
    }
]
```

### 2. Register a New User

### `/auth/register - POST`

**This endpoint is open and does not require a JWT token.**

#### Description:

Allows new users to register by providing a username, email, and password.

#### Required parameters:

- `username`: (`str`) The user's chosen username.
- `email`: (`str`) The user's email address.
- `password`: (`str`) The user's chosen password.

Example request:

```json
{
  "username": "newuser",
  "email": "newuser@email.com",
  "password": "password123"
}
```

#### Expected response:

JSON response of the created User object, 201.

Example response:

```json
{
  "id": 3,
  "username": "newuser",
  "email": "newuser@email.com",
  "role": "User",
  "date_created": "2024-03-22T10:00:00Z"
}
```

### 3. User Login

### `/auth/login - POST`

**This endpoint is open and does not require a JWT token.**

#### Description:

Authenticates a user by their email and password, returning a JWT token if successful.

#### Required parameters:

- `email`: (`str`) The user's email address.
- `password`: (`str`) The user's password.

Example request:

```json
{
  "email": "user@email.com",
  "password": "password123"
}
```

#### Expected response:

JSON object containing the user's email, JWT token, and role, 201

Example Response:

```json
{
  "email": "user@email.com",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "role": "User"
}
```

### 4. Delete a User (Admin only)

### `/auth/<int:user_id> - DELETE`

**This endpoint is protected and requires a valid JWT token. Only accessible by users with the "Admin" role.**

#### Description:

Deletes a specific user from the system.

#### Required parameters:

- `user_id`: URL parameter specifying the user's ID to be deleted.

#### Expected response:

Confirmation message of the deleted user, 201

Example response:

```json
{
  "message": "User 'newuser', 'User' deleted successfully"
}
```

</details>

## Category Controller:

<details>
  <summary>Click here for Category Controller Endpoints </summary>

### 1. Add a New Category for Future Transactions

### `/categories - POST`

**This endpoint is protected and requires a valid JWT token. Only users except those with the "Auditor" role can add categories.**

#### Description:

Allows creating a new category that can be assigned to future transactions.

#### Required parameters:

- `name`: (`str`) The name of the category.
- `description`: (`str`, optional) A description of the category.

Example request:

```json
{
  "name": "Utilities",
  "description": "Monthly bills for utilities"
}
```

#### Expected response:

JSON response of the created Category object, 201.

Example response:

```json
{
  "id": 1,
  "name": "Utilities",
  "description": "Monthly bills for utilities"
}
```

### 2. Get All Categories

### `/categories - GET`

**This endpoint is protected and requires a valid JWT token.**

#### Description:

Retrieves a list of all categories available in the system.

#### No parameters required.

#### Expected response:

JSON array of Category objects, 201

Example response:

```json
[
  {
    "id": 1,
    "name": "Utilities",
    "description": "Monthly bills for utilities"
  }
]
```


### 3. Get a Specific Category

### `/categories/<category_id> - GET`

**This endpoint is protected and requires a valid JWT token.**

#### Description:

Retrieves information about a specific category by its ID.

#### Required parameters:

- `category_id`: URL parameter specifying the category's ID.

#### Expected response:

JSON representation of the specified Category, 201

Example response:

```json
{
  "id": 1,
  "name": "Utilities",
  "description": "Monthly bills for utilities"
}
```

### 4. Update an Existing Category for Transactions

### `/categories/<category_id> - PUT/PATCH`

**This endpoint is protected and requires a valid JWT token. Only an Admin can update a category once created.**

#### Description:

Updates information about a specific category.

#### Required parameters:

- `name`: (`str`, optional) New name of the category.
- `description`: (`str`, optional) New description of the category.

#### Example request:

```json
{
  "name": "Monthly Utilities",
  "description": "Updated description for utilities"
}
```

#### Expected response:

JSON representation of the updated Category, 200.

Example response:

```json
{
  "id": 1,
  "name": "Monthly Utilities",
  "description": "Updated description for utilities"
}
```

### 5. Delete a category

### `/categories/<category_id> - DELETE`

**This endpoint is protected and requires a valid JWT token. Only an Admin can delete a category.**

#### Description:

Deletes a specific category from the system.

#### Required parameters:

- `category_id`: URL parameter specifying the category's ID to be deleted.

#### Expected response:

Confirmation message of the deleted category.

Example response:

```json
{
  "message": "Category with id 1, Name: Utilities, and Description: Monthly bills for utilities deleted successfully"
}
```

</details>

## Transaction Controller:

<details>
  <summary>Click here for Transaction Controller Endpoints </summary>

### 1. Add a New Transaction

### `/accounts/<int:account_id>/transactions - POST`

**This endpoint is protected and requires a valid JWT token.**

#### Description:

Allows adding a new transaction to a specific account. Users can add transactions only to their own accounts, except for admins who can add transactions to any account.

#### Required parameters for the account identified by <int:account_id>:

- `amount`: (`int`) The transaction amount. A positive value for deposits, negative for withdrawals.
- `description`: (`str`, optional) A description of the transaction.

Example request:

```json
{
  "amount": -50.75,
  "description": "Grocery shopping"
}
```

#### Expected response:

JSON response of the created Transaction object, 201.

Example response:

```json
{
  "id": 1,
  "amount": "-50.75",
  "description": "Grocery shopping",
  "transaction_date": "2024-03-23T12:00:00Z",
  "account_id": 1
}
```

### 2. Update an Existing Transaction (Admin Only)

### `/accounts/<int:account_id>/transactions/<int:transaction_id> - PUT/PATCH`

**This endpoint is protected and requires a valid JWT token. Only accessible by users with the "Admin" role.**

#### Description:

Updates information about a specific transaction within a specific account.

#### Required parameters:

- `amount`: (`int`, optional) New amount of the transaction.
- `description`: (`str`, optional) New description of the transaction.

Example request:

```json
{
  "amount": -45.0,
  "description": "Supermarket shopping"
}
```

#### Expected response:

JSON representation of the updated Transaction, 200.

Example response:

```json
{
  "id": 1,
  "amount": "-45.00",
  "description": "Supermarket shopping",
  "transaction_date": "2024-03-23T12:00:00Z",
  "account_id": 1
}
```

### 3. Delete a Transaction (Admin Only)

### `/accounts/<int:account_id>/transactions/<int:transaction_id> - DELETE`

**This endpoint is protected and requires a valid JWT token. Only accessible by users with the "Admin" role.**

#### Description:

Deletes a specific transaction from a specific account.

#### No parameters required beyond the URL parameters.

#### Expected response:

Confirmation message of the deleted transaction.

Example response:

```json
{
  "message": "Transaction with id 1, Description: 'Supermarket shopping', Amount: -45.00 deleted successfully"
}
```

### 4. Search Transactions (Role-Based Filtering)

### `/accounts/search - POST`

**This endpoint is protected and requires a valid JWT token.**

#### Description:

Searches transactions based on a description query. Auditors can see all transactions across all accounts, while other users can only see transactions within their own accounts.

### Required parameters:

- `query`: (`str`) The search term to match against transaction descriptions.
  Example request:

```json
{
  "query": "shopping"
}
```

#### Expected response:

JSON array of Transaction objects that match the search term.

Example response:

```json
[
  {
    "id": 1,
    "account_id": 1,
    "amount": "-45.00",
    "description": "Supermarket shopping",
    "transaction_date": "2024-03-23T12:00:00Z"
  }
]
```

</details>

</details>