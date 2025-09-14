#!/usr/bin/env python3
"""
This script demonstrates running multiple database queries concurrently using asyncio.gather.
"""

import asyncio
import aiosqlite
import os

DB_NAME = "test_3.db"

async def async_fetch_users():
    """Fetches all users from the database."""
    # Connect to the database
    async with aiosqlite.connect(DB_NAME) as db:
        # Execute the query
        async with db.execute("SELECT * FROM users") as cursor:
            # Fetch and print results
            results = await cursor.fetchall()
            print("Fetching all users...")
            print(results)
            return results

async def async_fetch_older_users():
    """Fetches users older than 40."""
    # Connect to the database
    async with aiosqlite.connect(DB_NAME) as db:
        # Execute the query with a parameter
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            # Fetch and print results
            results = await cursor.fetchall()
            print("Fetching users older than 40...")
            print(results)
            return results

async def fetch_concurrently():
    """Sets up the DB, executes queries concurrently, and cleans up."""
    # Setup a temporary database for the example
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
        await db.execute("INSERT INTO users (name, age) VALUES ('Allen', 30)")
        await db.execute("INSERT INTO users (name, age) VALUES ('Audrey', 45)")
        await db.execute("INSERT INTO users (name, age) VALUES ('Victor', 25)")
        await db.execute("INSERT INTO users (name, age) VALUES ('Faith', 50)")
        await db.commit()

    # Define the list of tasks to run concurrently
    tasks = [
        async_fetch_users(),
        async_fetch_older_users()
    ]
    
    # Execute tasks concurrently
    await asyncio.gather(*tasks)

    # Clean up the temporary database file
    os.remove(DB_NAME)

if __name__ == "__main__":
    # Run the main asynchronous function to fetch data concurrently
    asyncio.run(fetch_concurrently())
