#!/usr/bin/python3
"""
This module provides a generator for lazy pagination of user data.
"""

import seed

def paginate_users(page_size, offset):
    """Fetches a page of users from the database."""
    connection = seed.connect_to_prodev()
    if not connection:
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
        rows = cursor.fetchall()
        return rows
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def lazy_pagination(page_size):
    """
    Lazily fetches pages of users from the database.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
