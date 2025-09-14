#!/usr/bin/env python3
"""
This script demonstrates a reusable context manager for executing database queries.
"""

import sqlite3
import os

class ExecuteQuery:
    """
    A context manager to execute a given query and manage the connection.
    """
    def __init__(self, db_name, query, params=()):
        # Store database name, query, and parameters
        self.db_name = db_name
        self.query = query
        self.params = params
        self.conn = None

    def __enter__(self):
        # Establish connection and execute query
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        cursor.execute(self.query, self.params)
        results = cursor.fetchall()
        return results

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Ensure the connection is closed
        if self.conn:
            self.conn.close()

def main():
    """
    Main function to demonstrate the ExecuteQuery context manager.
    """
    db_file = "test_1.db"

    # Setup a temporary database for the example
    conn_setup = sqlite3.connect(db_file)
    cursor_setup = conn_setup.cursor()
    cursor_setup.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
    cursor_setup.execute("INSERT INTO users (name, age) VALUES ('Allen', 30)")
    cursor_setup.execute("INSERT INTO users (name, age) VALUES ('Victor', 25)")
    cursor_setup.execute("INSERT INTO users (name, age) VALUES ('Audrey', 40)")
    conn_setup.commit()
    conn_setup.close()

    # Define the query and parameters
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    # Use the context manager to execute the query
    with ExecuteQuery(db_file, query, params) as results:
        print(results)

    # Clean up the temporary database file
    os.remove(db_file)

if __name__ == "__main__":
    main()
