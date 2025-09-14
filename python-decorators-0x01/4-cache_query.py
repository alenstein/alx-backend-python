
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
        cursor.execute("INSERT INTO users (id, name, email) VALUES (1, 'Audrey', 'audrey@test.com')")
        cursor.execute("INSERT INTO users (id, name, email) VALUES (2, 'Harris', 'harris@test.com')")
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

# --- Cache Implementation ---

# A simple dictionary to act as an in-memory cache
query_cache = {}

def cache_query(func):
    """
    Decorator that caches the result of a function based on its arguments.
    For this specific use case, it caches based on the SQL query string.
    """
    @functools.wraps(func)
    def wrapper_cache_query(conn, *args, **kwargs):
        # Create a cache key from the query. The query is expected to be the first
        # positional arg after `conn` or a keyword arg named `query`.
        query = kwargs.get('query')
        if query is None:
            if args:
                query = args[0]
            else:
                # If no query is found, we cannot cache. Execute the function directly.
                return func(conn, *args, **kwargs)

        # Check if the result is already in the cache
        if query in query_cache:
            print(f"Cache hit! Returning cached result for query: {query}")
            return query_cache[query]

        # If not in cache, execute the function and store the result
        print(f"Cache miss. Executing query and caching result for: {query}")
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper_cache_query

# --- Decorated Function ---

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """
    Fetches users from the database. The result will be cached.
    """
    print("Executing database query...")
    cursor = conn.cursor()
    # Simulate a delay to emphasize the benefit of caching
    time.sleep(1)
    cursor.execute(query)
    results = cursor.fetchall()
    print("Query finished.")
    return results

# --- Main Execution ---
if __name__ == "__main__":
    setup_database()

    print("--- First Call (should execute and cache) ---")
    start_time = time.time()
    users = fetch_users_with_cache(query="SELECT * FROM users")
    duration = time.time() - start_time
    print(f"First call took {duration:.2f} seconds.")
    print("Users found:", users)
    print("-" * 20)

    print("\n--- Second Call (should be faster and hit cache) ---")
    start_time = time.time()
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    duration = time.time() - start_time
    print(f"Second call took {duration:.2f} seconds.")
    print("Users found again:", users_again)
    print("-" * 20)
    
    print("\n--- Third Call with different query (should execute and cache) ---")
    start_time = time.time()
    alice = fetch_users_with_cache(query="SELECT * FROM users WHERE name = 'Alice'")
    duration = time.time() - start_time
    print(f"Third call took {duration:.2f} seconds.")
    print("User 'Alice' found:", alice)
    print("-" * 20)

    # --- Cleanup ---
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
