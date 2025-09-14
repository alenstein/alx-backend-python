
import sqlite3
import functools
import os

# --- Database Setup ---
DB_FILE = 'users.db'

# Helper function to set up the database for the example
def setup_database():
    """Initializes a clean database for demonstration."""
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        # Added UNIQUE constraint to email to demonstrate rollback
        cursor.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT UNIQUE)')
        cursor.execute("INSERT INTO users (id, name, email) VALUES (1, 'Allen', 'allen@test.com')")
        conn.commit()
    finally:
        if conn:
            conn.close()

# --- Decorator Definitions ---

def with_db_connection(func):
    """
    Decorator that handles the database connection lifecycle.
    It creates a connection and passes it to the decorated function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = sqlite3.connect(DB_FILE)
            # Pass the connection object to the decorated function
            result = func(conn, *args, **kwargs)
            return result
        finally:
            if conn:
                conn.close()
    return wrapper

def transactional(func):
    """
    Decorator that wraps a function in a database transaction.
    Commits on success, rolls back on any exception.
    """
    @functools.wraps(func)
    def wrapper_transactional(conn, *args, **kwargs):
        try:
            # The wrapped function receives the connection from with_db_connection
            result = func(conn, *args, **kwargs)
            conn.commit()
            print("Transaction committed successfully.")
            return result
        except Exception as e:
            print(f"An error occurred: {e}. Rolling back transaction.")
            if conn:
                conn.rollback()
            # Re-raise the exception to let the caller know something went wrong
            raise
    return wrapper_transactional

# --- Decorated Functions for Demonstration ---

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """Updates a user's email within a transaction."""
    print(f"Attempting to update user {user_id}'s email to {new_email}...")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

@with_db_connection
def get_user(conn, user_id):
    """Helper function to fetch a user and verify changes."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# --- Main Execution ---
if __name__ == "__main__":
    setup_database()

    print("--- Initial State ---")
    user_before = get_user(user_id=1)
    print(f"User 1: {user_before}")
    print("-" * 20)

    print("\n--- Demonstrating a Successful Transaction ---")
    try:
        update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
    except Exception as e:
        print(f"Update failed with an unexpected error: {e}")
    
    print("\n--- State After Successful Update ---")
    user_after_success = get_user(user_id=1)
    print(f"User 1: {user_after_success}")
    print("-" * 20)

    # --- 2. Demonstrate a Failed Transaction (Rollback) ---
    print("\n--- Demonstrating a Failed Transaction (Rollback) ---")
    print("Attempting to update email to a value that will cause a UNIQUE constraint error...")
    setup_database() # Reset DB for a clean test
    # Add a second user to create a conflict
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("INSERT INTO users (id, name, email) VALUES (2, 'Bob', 'bob@example.com')")
        conn.commit()

    print("\n--- State Before Failed Update ---")
    user_before_fail = get_user(user_id=1)
    print(f"User 1: {user_before_fail}")
    
    try:
        # This will fail because 'bob@example.com' is already taken by user 2
        update_user_email(user_id=1, new_email='sibs@test.com')
    except sqlite3.IntegrityError:
        # This exception is expected
        print("Caught expected IntegrityError.")

    print("\n--- State After Failed Update ---")
    user_after_fail = get_user(user_id=1)
    print(f"User 1 (should be unchanged): {user_after_fail}")
    print("-" * 20)

    # --- Cleanup ---
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
