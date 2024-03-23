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

# Coder Academy - T2A2 - Webserver API Project Response:
Links:

- [GitHub](https://github.com/xdaybreakerx/XanderSalathe_T2A2)
- [Trello](https://trello.com/b/8Lz0gZWa/xander-salathe-t2a2-api-webserver)

## R1 Identification of the problem you are trying to solve by building this particular app.
<details>
  <summary>Click here for response </summary>

The core problem this app aims to solve revolves around financial management and oversight, particularly in tracking and categorizing transactions across various accounts. Users, ranging from individuals to small business owners, often struggle with managing their finances due to the complexity of handling multiple accounts, understanding spending habits, and maintaining a budget. This app facilitates the organization, tracking, and analysis of financial transactions by categorizing them and providing a comprehensive view of financial activities across different accounts.

The application serves as a centralized platform where users can view all their financial transactions in one place, categorize them for better financial planning and analysis, and ensure sensitive financial data is handled securely. Additionally, the app supports role-based access, allowing for an auditor role that can review transactions across all accounts, catering to businesses or families where financial oversight is shared or delegated.
</details>

## R2 Why is it a problem that needs solving?
<details>
  <summary>Click here for response </summary>
Managing finances, especially when dealing with multiple accounts and transaction types, can be daunting and time-consuming. Without a centralized system, individuals and businesses may struggle to get a clear picture of their financial health, leading to poor financial decisions, budgeting failures, and potentially, financial instability.

- Complexity and Time-Consumption: Manually tracking and categorizing transactions across different platforms or accounts is inefficient and prone to errors. An app that automates and centralizes this process saves time and reduces errors, making financial management more accessible and less daunting.

- Financial Oversight: For individuals, understanding where their money is going is crucial for effective budgeting and savings plans. For businesses or families, being able to audit finances transparently and securely is vital for trust and financial integrity. This app addresses these needs by providing detailed transaction tracking, categorization, and role-based access for auditing purposes.

- Accessibility and Usability: Financial management tools often require financial literacy or familiarity with financial jargon, which can be a barrier for many users. An app that simplifies these processes and presents financial data in a user-friendly manner can democratize financial management, making it accessible to a wider audience with varying levels of financial expertise.

- Data Security: Financial data is sensitive and requires stringent security measures. Traditional or manual methods of tracking finances may not offer adequate data protection. This app emphasizes secure handling of financial data, with features like role-based access control and secure authentication, ensuring users' financial data is protected against unauthorized access.

By solving these problems, the app not only makes financial management more efficient and less error-prone but also promotes better financial habits, informed decision-making, and financial stability for its users.

</details>

## R3 Why have you chosen this database system. What are the drawbacks compared to others?
<details>
  <summary>Click here for response </summary>
In the context of this financial transaction management app, PostgreSQL has been chosen for its robustness, reliability, and support for complex data structures and relationships, which are essential for accurately modeling and querying financial data. The application requires managing detailed records of transactions, accounts, users, and potentially categories, each with their specific attributes and relationships (e.g., users having multiple accounts, transactions belonging to specific accounts).

Specific Implementation with SQLAlchemy:

Data Integrity and Relationships: Using SQLAlchemy, the app defines models such as User, Account, Transaction, and Category, each represented as a Python class. These models are directly mapped to PostgreSQL tables, allowing the application to enforce data integrity through foreign keys and constraints. For instance, the ForeignKey constraint is used to link transactions to their respective accounts and categories, ensuring data consistency.

Complex Queries: The application leverages SQLAlchemy's rich query API to perform complex queries, such as filtering transactions by account, searching transactions based on descriptions (using ilike for case-insensitive matching), and ranking transactions within accounts. These operations benefit from PostgreSQL's capabilities and are easily constructed through SQLAlchemy's expressive syntax.

Role-Based Access Control: The application's requirement for different access levels based on user roles (e.g., regular users vs. auditors) is facilitated by SQLAlchemy's ability to filter query results based on the user's role and associated accounts, demonstrating a sophisticated understanding of both database querying and application-level security considerations.

For this project, PostgreSQL, a powerful, open-source object-relational database system, has been chosen due to its strong reputation for reliability, feature robustness, and performance. It offers advanced features such as complex queries, foreign keys, triggers, views, transactional integrity, and multiversion concurrency control. PostgreSQL is well-suited for applications requiring complex data relationships and integrity, making it ideal for managing financial transactions where accuracy and data relationships are critical.

Drawbacks Compared to Others:

Complexity: For smaller projects or applications with simpler data storage needs, PostgreSQL might introduce unnecessary complexity compared to lightweight alternatives like SQLite.
Performance Overhead: While highly scalable, PostgreSQL may introduce more overhead than NoSQL databases like MongoDB in scenarios requiring high write throughput and horizontal scaling.
Learning Curve: Its extensive feature set and capabilities might present a steeper learning curve compared to simpler databases, potentially delaying development for teams less familiar with relational database concepts.

</details>

## R4 Identify and discuss the key functionalities and benefits of an ORM
<details>
  <summary>Click here for response </summary>

Object-Relational Mapping (ORM) is a technique that connects the rich object-oriented world of application code to the relational world of databases. SQLAlchemy, the ORM chosen for this project, offers several key functionalities and benefits:

Abstraction and Ease of Use: ORM allows developers to interact with the database using high-level entities such as classes and objects instead of writing SQL queries, making data operations more intuitive and less error-prone.
Data Model as Code: It enables defining the database schema as Python classes, making it easier to understand, maintain, and evolve the database structure alongside the application code.
Query Composition: SQLAlchemy provides a powerful query composition API, allowing complex queries to be constructed programmatically and reused, enhancing code readability and maintainability.
Automatic Schema Migration: Tools like Alembic, integrated with SQLAlchemy, facilitate schema migrations, helping manage database evolution without manual intervention.
Database Agnosticism: ORM abstracts the underlying database system, making it easier to switch between different databases with minimal changes to the application code.
Data Integrity and Security: By avoiding manual string concatenation for SQL queries, ORMs like SQLAlchemy help prevent SQL injection attacks and ensure data integrity through declarative constraints and transaction management.
While ORMs offer powerful advantages, it's important to be mindful of potential drawbacks such as the overhead of abstraction, which might affect performance in high-load scenarios, and the complexity of mapping highly normalized data structures or optimizing certain types of queries. Balancing these considerations is key to leveraging ORMs effectively in application development.

Abstraction and Ease of Use: SQLAlchemy abstracts the underlying PostgreSQL database, allowing the app to interact with it through high-level Python objects instead of raw SQL. This makes the code more readable and maintainable, especially when dealing with complex financial data.

Automated Schema Management: The app benefits from SQLAlchemy's support for schema migrations through Alembic, enabling automated management of database schema changes as the application evolves. This is crucial for financial applications where the data model might need to adapt over time without losing data integrity.

Security: By using SQLAlchemy's query builder, the app avoids concatenating SQL queries manually, significantly reducing the risk of SQL injection attacks. This security feature is particularly important in financial applications where data integrity and security are paramount.

Performance Optimization: Although ORMs can introduce some overhead, SQLAlchemy allows for fine-tuning queries and leveraging PostgreSQL's advanced features when needed. This means the app can balance ease of development with performance, optimizing queries for critical operations such as transaction searches and reporting.

Data Manipulation and Retrieval: The app utilizes SQLAlchemy for CRUD operations on financial transactions, user accounts, etc., leveraging session management for transactional integrity. This ensures that operations like creating a new account, recording a transaction, or updating account balances are performed reliably.

In summary, SQLAlchemy's implementation in this financial transaction management app exemplifies how an ORM can streamline development, enhance security, and provide flexibility for complex data interactions, all while leveraging the strengths of a robust database system like PostgreSQL.

</details>

## R5 Document all endpoints for your API

<details>
  <summary>Click here for response </summary>

## Account Controller:
<details>
  <summary>Click here for Account Controller Endpoints </summary>

### 1. Create a New Account

### `/accounts - POST`

**This endpoint is protected and requires a valid JWT token.**

#### _Description:_

Used to create a new Account in relation to a User

#### _Required parameters:_

- `account_type`: (`str`) type or description of account
- `balance`: (`int`) initial value of account

eg

```json
{
  "account_type": "savings",
  "balance": 15000
}
```

#### _Expected response:_

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

#### _Authentication:_

JWT

#### _SQL Query_

```sql
INSERT INTO accounts (account_type, balance, user_id) VALUES (?, ?, ?);
```

### 2. Get a List of All Accounts (with Role-Based Filtering) - Auditor

### `/accounts - GET`

**This endpoint is protected and requires a valid JWT token.**

#### _Description:_

Retrieves a list of all accounts. Auditors can see all accounts, while other users see only their own.

No parameters required.

#### _Expected response:_

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

#### _SQL Query for Auditor_

```sql
SELECT * FROM accounts ORDER BY date_created DESC;
```

#### _SQL Query for Regular Users_

```sql
SELECT * FROM accounts WHERE user_id = ?
ORDER BY date_created DESC;
```

### 3. Get a Specific Account

### `/accounts/<account_id> - GET`

**This endpoint is protected and requires a valid JWT token.**

_Description:_

Retrieves information about a specific account. Auditors can view any account, while other users can only view their own accounts.

_Required parameters_:

- `account_id`: URL parameter specifying the account's ID.

_Expected response_:

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

_Authentication:_

JWT

_SQL Query_

```sql
SELECT * FROM accounts WHERE id = ?;
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

#### _Authentication_:

JWT

#### _SQL Query_

```sql
UPDATE accounts SET account_type = ?, balance = ? WHERE id = ?;
```

### 5. Delete an Existing Account

### `/accounts/<account_id> - DELETE`

_This endpoint is protected and requires a valid JWT token. Only Admins can delete accounts not owned by themselves._

#### _Description:_

Deletes a specific account.

#### _Required parameters:_

- `account_id`: URL parameter specifying the account's ID.

#### _Expected response:_

Confirmation message of the deleted account, 201

_Example response:_

```json
{
  "message": "Account 'emergency fund' deleted successfully"
}
```

#### _Authentication:_

JWT

#### _SQL Query_

```sql
DELETE FROM accounts WHERE id = ?;
```

### 6. Get Total Balance (Auditor Only)

### `/accounts/total_balance - GET`

**This endpoint is protected and requires a valid JWT token. Only accessible by users with the "Auditor" role.**

Description: Calculates the total balance across all accounts in the system.

No parameters required.

Expected response: JSON object with the total balance.

Example response:

```json
{
  "total_balance": "27345.01"
}
```

Authentication: JWT

SQL Query

```sql
SELECT SUM(balance) FROM accounts;
```

### 7. Rank Transactions within an Account (Auditor Only)

### `/accounts/<int:account_id>/transactions/rank - GET`

**This endpoint is protected and requires a valid JWT token. Only accessible by users with the "Auditor" role.**

Description: Ranks transactions within a specific account based on the amount, showing the relative size of each transaction.

Required parameters:

account_id: URL parameter specifying the account's ID to rank transactions within.
Expected response: JSON array of transactions with their ranks.

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
Authentication: JWT

SQL Query:
Ranking transactions requires the use of window functions, which are not straightforwardly represented in raw SQL without the specific database context. Here is a conceptual example

```sql
SELECT id, amount, RANK()
OVER (PARTITION BY account_id ORDER BY amount DESC)
FROM transactions WHERE account_id = ?;
```

### 8. Account Summary (Auditor Only)

### `/accounts/summary - GET`

**This endpoint is protected and requires a valid JWT token. Only accessible by users with the "Auditor" role.**
Description: Provides a summary of each account including the account ID, type, and total spent in transactions.

No parameters required.

Expected response: JSON array with a summary for each account.

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

Authentication: JWT

SQL Query

```sql
WITH account_summary AS (
    SELECT accounts.id AS account_id, SUM(transactions.amount) AS total_spent
    FROM accounts
    JOIN transactions ON accounts.id = transactions.account_id
    GROUP BY accounts.id
)
SELECT account_id, account_type, total_spent FROM account_summary
JOIN accounts ON accounts.id = account_summary.account_id;
```

### 9. Search Transactions (with Role-Based Filtering) - Auditor
### ```/accounts/search - POST```
**This endpoint is protected and requires a valid JWT token. It enables searching for transactions based on a description, with results filtered by the user's role.**

Description: Allows users to search for transactions across all accounts if they have the "Auditor" role. Regular users can only search within their own accounts.

Required parameters (in JSON body):

- ```query```: (```str```) The search term to filter transactions by their description.
Example request:
```json
{
    "query": "groceries"
}
```
Expected response: JSON array of transactions matching the search term, filtered according to the user's role.

Example response (for an "Auditor"):

Expected response: JSON array of transactions matching the search term, filtered according to the user's role.

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
Authentication: JWT


SQL Query for Auditor:

```sql
SELECT * FROM transactions
JOIN accounts ON transactions.account_id = accounts.id
WHERE transactions.description ILIKE '%groceries%';
```

SQL Query for user: 
```sql
SELECT * FROM transactions
JOIN accounts ON transactions.account_id = accounts.id
WHERE transactions.description ILIKE '%groceries%' AND accounts.user_id = ?;
```

</details>

## Auth Controller:
<details>
  <summary>Click here for Auth Controller Endpoints </summary>

### 1. Get All Users (Auditor Only)
### `/auth/users - GET`
**This endpoint is protected and requires a valid JWT token. Only accessible by users with the "Auditor" role.**
Description: Retrieves a list of all registered users in the system.

No parameters required.

Expected response: JSON array of User objects.

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
Authentication: JWT

SQL Query

```sql
SELECT * FROM users ORDER BY date_created DESC;
```

### 2. Register a New User
### `/auth/register - POST`
**This endpoint is open and does not require a JWT token.**
Description: Allows new users to register by providing a username, email, and password.

Required parameters:

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
Expected response: JSON response of the created User object, 201.

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


SQL Query


```sql
-- password hashed before insertion into DB
INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?);
```

### 3. User Login
### `/auth/login - POST`
**This endpoint is open and does not require a JWT token.**
Description: Authenticates a user by their email and password, returning a JWT token if successful.

Required parameters:

- `email`: (`str`) The user's email address.
- `password`: (`str`) The user's password.
Example request:
```json
{
    "email": "user@email.com",
    "password": "password123"
}
```
Expected response: JSON object containing the user's email, JWT token, and role.

```json
{
    "email": "user@email.com",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "role": "User"
}
```

SQL Query

```sql
SELECT * FROM users WHERE email = ?;
-- Password verification and JWT creation occur in the application layer.
```

### 4. Delete a User (Admin only)
### `/auth/<int:user_id> - DELETE`
**This endpoint is protected and requires a valid JWT token. Only accessible by users with the "Admin" role.**

Description: Deletes a specific user from the system.

Required parameters:

- `user_id`: URL parameter specifying the user's ID to be deleted.

Expected response: Confirmation message of the deleted user, 201

Example response:
```json
{
    "message": "User 'newuser', 'User' deleted successfully"
}
```
Authentication: JWT

SQL Query

```sql
DELETE FROM users WHERE id = ?;
```
</details>


## Category Controller:
<details>
  <summary>Click here for Category Controller Endpoints </summary>

### 1. Add a New Category for Future Transactions
### /categories - POST

**This endpoint is protected and requires a valid JWT token. Only users except those with the "Auditor" role can add categories.**

Description: Allows creating a new category that can be assigned to future transactions.

Required parameters:

- `name`: (`str`) The name of the category.
- `description`: (`str`, optional) A description of the category.
Example request:
```json
{
    "name": "Utilities",
    "description": "Monthly bills for utilities"
}
```
Expected response: JSON response of the created Category object, 201.
Example response:
```json
{
    "id": 1,
    "name": "Utilities",
    "description": "Monthly bills for utilities"
}
```

Authentication: JWT
SQL Query

```sql
--  Before inserting a new category, an existence check is performed:
SELECT * FROM categories WHERE name = ?;
-- If the category doesn't exist, then:
INSERT INTO categories (name, description) VALUES (?, ?);
```

### 2. Get All Categories
### `/categories - GET`
**This endpoint is protected and requires a valid JWT token.**

Description: Retrieves a list of all categories available in the system.

No parameters required.

Expected response: JSON array of Category objects.

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
Authentication: JWT


SQL Query

```sql
SELECT * FROM categories;
```

### 3. Get a Specific Category
### /categories/<category_id> - GET
**This endpoint is protected and requires a valid JWT token.**
Description: Retrieves information about a specific category by its ID.

Required parameters:

- `category_id`: URL parameter specifying the category's ID.
Expected response: JSON representation of the specified Category.

Example response:
```json
{
    "id": 1,
    "name": "Utilities",
    "description": "Monthly bills for utilities"
}
```
Authentication: JWT

SQL Query

```sql
SELECT * FROM categories WHERE id = ?;
```

### 4. Update an Existing Category for Transactions
### `/categories/<category_id> - PUT/PATCH`
**This endpoint is protected and requires a valid JWT token. Only an Admin can update a category once created.**
Description: Updates information about a specific category.

Required parameters:

- `name`: (`str`, optional) New name of the category.
- `description`: (`str`, optional) New description of the category.
Example request:
```json
{
    "name": "Monthly Utilities",
    "description": "Updated description for utilities"
}
```
Expected response: JSON representation of the updated Category, 200.
Example response:
```json
{
    "id": 1,
    "name": "Monthly Utilities",
    "description": "Updated description for utilities"
}
```
Authentication: JWT

SQL Query

```sql
-- check for name uniqueness excluding the current category
SELECT * FROM categories WHERE name = ? AND id <> ?;
-- if check passes then:
UPDATE categories SET name = ?, description = ? WHERE id = ?;
```

### 5. Delete a category
### `/categories/<category_id> - DELETE`
**This endpoint is protected and requires a valid JWT token. Only an Admin can delete a category.**
Description: Deletes a specific category from the system.

Required parameters:

- `category_id`: URL parameter specifying the category's ID to be deleted.

Expected response: Confirmation message of the deleted category.

Example response:
```json
{
    "message": "Category with id 1, Name: Utilities, and Description: Monthly bills for utilities deleted successfully"
}
```

SQL Query

```sql
DELETE FROM categories WHERE id = ?;
```

</details>

## Transaction Controller:

<details>
  <summary>Click here for Transaction Controller Endpoints </summary>

### 1. Add a New Transaction
### `/accounts/<int:account_id>/transactions - POST`
**This endpoint is protected and requires a valid JWT token.**
Description: Allows adding a new transaction to a specific account. Users can add transactions only to their own accounts, except for admins who can add transactions to any account.

Required parameters for the account identified by <int:account_id>:

- `amount`: (`int`) The transaction amount. A positive value for deposits, negative for withdrawals.
- `description`: (`str`, optional) A description of the transaction.
Example request:
```json
{
    "amount": -50.75,
    "description": "Grocery shopping"
}
```
Expected response: JSON response of the created Transaction object, 201.
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
Authentication: JWT

SQL Query

```sql
-- Before inserting a new transaction, check if the account exists and if the user has the right to add transactions to it
SELECT * FROM accounts WHERE id = ?;
-- If the account exists and the user has the right to access it:
INSERT INTO transactions (amount, description, account_id) VALUES (?, ?, ?);
-- Then, update the account balance:
UPDATE accounts SET balance = balance + ? WHERE id = ?;
```

### 2. Update an Existing Transaction (Admin Only)
### `/accounts/<int:account_id>/transactions/<int:transaction_id> - PUT/PATCH`
**This endpoint is protected and requires a valid JWT token. Only accessible by users with the "Admin" role.**
Description: Updates information about a specific transaction within a specific account.

Required parameters:

- `amount`: (`int`, optional) New amount of the transaction.
- `description`: (`str`, optional) New description of the transaction.
Example request:
```json
{
    "amount": -45.00,
    "description": "Supermarket shopping"
}
```
Expected response: JSON representation of the updated Transaction, 200.

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
Authentication: JWT

SQL Query

```sql
-- To update an existing transaction (only by an Admin), first, the transaction is selected:
SELECT * FROM transactions WHERE id = ? AND account_id = ?;
-- If the transaction exists, update it:
UPDATE transactions SET amount = ?, description = ? WHERE id = ?;
-- Additionally, adjust the account balance by the difference between the old and new transaction amounts:
UPDATE accounts SET balance = balance + (? - old_amount) WHERE id = ?;
```

### 3. Delete a Transaction (Admin Only)
### `/accounts/<int:account_id>/transactions/<int:transaction_id> - DELETE`
**This endpoint is protected and requires a valid JWT token. Only accessible by users with the "Admin" role.**

Description: Deletes a specific transaction from a specific account.

No parameters required beyond the URL parameters.

Expected response: Confirmation message of the deleted transaction.

Example response:
```json
{
    "message": "Transaction with id 1, Description: 'Supermarket shopping', Amount: -45.00 deleted successfully"
}
```
Authentication: JWT

SQL Query

```sql
-- Similar to updating, first, select the transaction to be deleted:
SELECT * FROM transactions WHERE id = ? AND account_id = ?;
-- If found, delete the transaction:
DELETE FROM transactions WHERE id = ?;
-- Then, adjust the account's balance to subtract the transaction's amount:
UPDATE accounts SET balance = balance - ? WHERE id = ?;
```

### 4. Search Transactions (Role-Based Filtering)
### `/accounts/search - POST`
**This endpoint is protected and requires a valid JWT token.**
Description: Searches transactions based on a description query. Auditors can see all transactions across all accounts, while other users can only see transactions within their own accounts.

Required parameters:

- `query`: (`str`) The search term to match against transaction descriptions.
Example request:
```json
{
    "query": "shopping"
}
```
Expected response: JSON array of Transaction objects that match the search term.

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
Authentication: JWT
SQL Query for an Auditor:

```SQL
SELECT * FROM transactions WHERE description ILIKE '%shopping%';
```
SQL Query for a regular user:
```SQL
SELECT t.* FROM transactions t
JOIN accounts a ON t.account_id = a.id
WHERE a.user_id = ? AND t.description ILIKE '%shopping%';
```
</details>

</details>

## R6 An ERD for your app
<details>
  <summary>Click here for response </summary>

![erd](../../docs/erd.png)

</details>

## R7 Detail any third-party services that your app will use
<details>
  <summary>Click here for response </summary>

| Service                | Description                                                                                                             |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Flask                  | Micro web framework for Python used to build web applications. Provides tools, libraries for web tasks.                 |
| PostgreSQL (neon.tech) | Neon.tech is a PostgreSQL as a service host provider. PostgreSQL is a powerful, open-source relational database system. |
| bcrypt                 | Provides hashing utilities for passwords, ensuring secure storage.                                                      |
| bleach                 | A library for sanitizing and linkifying text from potentially unsafe sources, preventing XSS attacks.                   |
| blinker                | Provides support for signals, allowing Flask extensions to communicate changes or events.                               |
| Flask-Bcrypt           | Flask extension that provides Bcrypt hashing utilities for your application.                                            |
| Flask-JWT-Extended     | Extends Flask to support JSON Web Tokens (JWT) for secure authentication.                                               |
| flask-marshmallow      | Integrates Flask with Marshmallow for object serialization and deserialization, ORM integration.                        |
| Flask-SQLAlchemy       | Adds SQLAlchemy support to Flask applications for ORM use with models and queries.                                      |
| marshmallow            | An ORM/ODM/framework-agnostic library for object serialization and deserialization.                                     |
| marshmallow-sqlalchemy | SQLAlchemy integration with Marshmallow for easily converting database models into schemas.                             |
| psycopg2-binary        | PostgreSQL database adapter for Python. Allows connection and manipulation of PostgreSQL databases.                     |
| python-dotenv          | Reads key-value pairs from a `.env` file and sets them as environment variables.                                        |
| SQLAlchemy             | SQL toolkit and ORM for Python, provides full power and flexibility of SQL.                                             |
</details>

## R8 Describe your projects models in terms of the relationships they have with each other
<details>
  <summary>Click here for response </summary>
</details>

## R9 Discuss the database relations to be implemented in your application

<details>
  <summary>Click here for response </summary>
</details>

## R10 Describe the way tasks are allocated and tracked in your project

<details>
  <summary>Click here for response </summary>
</details>
