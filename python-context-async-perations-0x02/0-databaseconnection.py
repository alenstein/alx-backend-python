#!/usr/bin/env python3
"""
This script demonstrates a class-based context manager for managing database
connections.
"""

import sqlite3
import os

class DatabaseConnection:
    """
    A context manager to handle opening and closing a database connection.
    """
    def __init__(self, db_name):
        # Store the database file name
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        # Establish the database connection
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Ensure the connection is closed
        if self.conn:
            self.conn.close()

def main():
    """
    Main function to demonstrate the DatabaseConnection context manager.
    """
    db_file = "test.db"

    # Setup a temporary database for the example
    conn_setup = sqlite3.connect(db_file)
    cursor_setup = conn_setup.cursor()
    cursor_setup.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
    cursor_setup.execute("INSERT INTO users (name) VALUES ('Alice')")
    cursor_setup.execute("INSERT INTO users (name) VALUES ('Bob')")
    conn_setup.commit()
    conn_setup.close()

    # Use the context manager to perform a query
    with DatabaseConnection(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print(results)

    # Clean up the temporary database file
    os.remove(db_file)

if __name__ == "__main__":
    main()
