#!/usr/bin/env python3
"""
This module provides a class-based context manager for managing database connections.
"""

import sqlite3

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
