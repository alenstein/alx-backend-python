#!/usr/bin/python3
"""
This module provides functions to interact with a MySQL database,
including connecting to the server, creating a database and table,
and inserting data from a CSV file.
"""

import mysql.connector
import csv
import os


def connect_db():
    """Connects to the MySQL database server."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASS', '')
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None


def create_database(connection):
    """Creates the database ALX_prodev if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev created successfully or already exists.")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")


def connect_to_prodev():
    """Connects to the ALX_prodev database in MySQL."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASS', ''),
            database='ALX_prodev'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev: {err}")
        return None


def create_table(connection):
    """Creates a table user_data if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(255) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL
            )
        """)
        print("Table user_data created successfully")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")


def insert_data(connection, data_file):
    """Inserts data in the database if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM user_data")
        if cursor.fetchone()[0] > 0:
            print("Data already exists in user_data table.")
            cursor.close()
            return

        with open(data_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                cursor.execute(
                    "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                    (row[0], row[1], row[2], row[3])
                )
        connection.commit()
        print("Data inserted successfully.")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
    except FileNotFoundError:
        print(f"Error: {data_file} not found.")
