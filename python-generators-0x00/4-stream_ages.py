#!/usr/bin/python3
"""
This module provides a memory-efficient way to calculate the average age
of users from a database using generators.
"""

from seed import connect_to_prodev

def stream_user_ages():
    """Yields user ages one by one from the database."""
    connection = connect_to_prodev()
    if not connection:
        return

    try:
        # Use a server-side cursor for large datasets if supported
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")
        for row in cursor:
            yield row[0]
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def calculate_average_age():
    """
    Calculates the average age from the stream of user ages.
    """
    total_age = 0
    user_count = 0
    age_generator = stream_user_ages()

    for age in age_generator:
        total_age += age
        user_count += 1

    if user_count > 0:
        average_age = total_age / user_count
        print(f"Average age of users: {average_age:.2f}")
    else:
        print("No users found.")

if __name__ == "__main__":
    calculate_average_age()
