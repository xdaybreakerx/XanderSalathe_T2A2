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