import sqlite3
import functools
import os


# Define the decorator to log SQL queries
def log_queries(func):
    """
    Decorator that logs the SQL query before executing the function it decorates.
    """

    @functools.wraps(func)
    def wrapper_log_queries(*args, **kwargs):
        query = kwargs.get('query')
        if query is None and args:
            query = args[0]

        print(f"Executing query: {query}")

        # Execute the original function and return its result
        return func(*args, **kwargs)

    return wrapper_log_queries



# Name of the database file
DB_FILE = 'users.db'

# Clean up previous database file if it exists
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)

# Setup a dummy database for the example to work
try:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # Create the users table
    cursor.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)')
    # Insert some data
    cursor.execute("INSERT INTO users (id, name, email) VALUES (1, 'TestUser0', 'user0@test.com')")
    cursor.execute("INSERT INTO users (id, name, email) VALUES (2, 'TestUser1', 'user1@etest.com')")
    conn.commit()
finally:
    conn.close()


# --- Original code from the problem description ---

@log_queries
def fetch_all_users(query):
    """
    Connects to the database, executes a query, and fetches all results.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# Fetch users while logging the query
print("Fetching users...")
users = fetch_all_users(query="SELECT * FROM users")
print("Result:")
print(users)

# --- Cleanup ---
# Clean up the created database file
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
