#!/usr/bin/python3
"""
This module provides functions for batch processing of user data
from a MySQL database.
"""

from seed import connect_to_prodev

def stream_users_in_batches(batch_size=50):
    """
    Fetches users from the database in batches and yields them.
    """
    connection = connect_to_prodev()
    if not connection:
        return

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def batch_processing(batch_size=50):
    """
    Processes user batches to filter users over the age of 25.
    """
    user_stream = stream_users_in_batches(batch_size)
    for batch in user_stream:
        for user in batch:
            if user['age'] > 25:
                print(user)
