
import sqlite3
import functools
import os

# --- Database Setup ---
DB_FILE = 'users.db'

# Clean up previous database file if it exists
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)

# Setup a dummy database for the example
try:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # Create the users table
    cursor.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)')
    # Insert some data
    cursor.execute("INSERT INTO users (id, name, email) VALUES (1, 'Alice', 'alice@example.com')")
    cursor.execute("INSERT INTO users (id, name, email) VALUES (2, 'Bob', 'bob@example.com')")
    conn.commit()
finally:
    conn.close()

# --- Decorator Definition ---

def with_db_connection(func):
    """
    Decorator that opens a database connection, passes it to the decorated function,
    and ensures the connection is closed afterward.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = sqlite3.connect(DB_FILE)
            result = func(conn, *args, **kwargs)
            return result
        finally:
            if conn:
                conn.close()
    return wrapper

# --- Decorated Function ---

@with_db_connection
def get_user_by_id(conn, user_id):
    """
    Fetches a user from the database by their ID using the provided connection.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# --- Execution ---

# Fetch user by ID with automatic connection handling
print("Fetching user with id 1...")
user = get_user_by_id(user_id=1)
print(user)

# --- Cleanup ---
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
