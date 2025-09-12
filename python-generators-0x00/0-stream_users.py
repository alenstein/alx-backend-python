#!/usr/bin/python3
"""
This module provides a generator function to stream users from a database.
"""

from seed import connect_to_prodev

def stream_users():
    """
    Fetches users from the database one by one and yields them.
    """
    connection = connect_to_prodev()
    if not connection:
        return

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        for row in cursor:
            yield row
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
