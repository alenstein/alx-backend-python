
import time
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
        cursor.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)')
        cursor.execute("INSERT INTO users (id, name, email) VALUES (1, 'Victor', 'victor@test.com')")
        conn.commit()
    finally:
        if conn:
            conn.close()

# --- Decorator Definitions ---

def with_db_connection(func):
    """
    Decorator that handles the database connection lifecycle.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = sqlite3.connect(DB_FILE)
            # Pass the connection object to the decorated function
            return func(conn, *args, **kwargs)
        finally:
            if conn:
                conn.close()
    return wrapper

def retry_on_failure(retries=3, delay=1):
    """
    A decorator factory that retries a function if it raises an exception.
    
    Args:
        retries (int): The maximum number of times to retry.
        delay (int): The number of seconds to wait between retries.
    """
    def decorator_retry(func):
        @functools.wraps(func)
        def wrapper_retry(*args, **kwargs):
            last_exception = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"Attempt {attempt + 1} of {retries} failed: {e}")
                    print(f"Retrying in {delay} second(s)...")
                    time.sleep(delay)
            # If all retries fail, raise the last captured exception
            if last_exception is not None:
                raise last_exception
        return wrapper_retry
    return decorator_retry


# Global counter to simulate transient failures
ATTEMPT_COUNTER = 0

@with_db_connection
@retry_on_failure(retries=4, delay=1) # Set retries to 4 to succeed on the 3rd attempt
def fetch_users_with_retry(conn):
    """
    A function that simulates failure on its first two attempts.
    """
    global ATTEMPT_COUNTER
    ATTEMPT_COUNTER += 1
    print(f"--- Attempting to fetch users (Attempt #{ATTEMPT_COUNTER}) ---")

    # Simulate a failure on the first 2 attempts
    if ATTEMPT_COUNTER < 3:
        raise sqlite3.OperationalError("Simulated database connection error")

    print("Connection successful!")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# --- Main Execution ---
if __name__ == "__main__":
    setup_database()

    print("Attempting to fetch users with a function that fails initially...")
    try:
        users = fetch_users_with_retry()
        print("\nSuccessfully fetched users after retries:")
        print(users)
    except Exception as e:
        print(f"\nFunction failed after all retries: {e}")

    # --- Cleanup ---
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
