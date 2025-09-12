# Python Generators 0x00

This project demonstrates the use of Python generators to stream data from a MySQL database.

## Files

* `seed.py`: A Python script to set up and populate the `ALX_prodev` database with sample data from `user_data.csv`.
* `0-main.py`: A script to test the functionality of `seed.py`.
* `user_data.csv`: A CSV file containing sample user data.

## Requirements

* Python 3
* `mysql-connector-python` library
* A running MySQL server

## Setup

1. **Install the required library:**
   ```bash
   pip install mysql-connector-python
   ```

2. **Set up environment variables (optional):**
   You can set the following environment variables to configure the database connection:
   * `DB_USER`: Your MySQL username (default: `root`)
   * `DB_PASS`: Your MySQL password (default: ``)

3. **Run the main script:**
   ```bash
   ./0-main.py
   ```

## `seed.py` Functions

* `connect_db()`: Connects to the MySQL database server.
* `create_database(connection)`: Creates the `ALX_prodev` database if it doesn't exist.
* `connect_to_prodev()`: Connects to the `ALX_prodev` database.
* `create_table(connection)`: Creates the `user_data` table if it doesn't exist.
* `insert_data(connection, data_file)`: Inserts data from a CSV file into the `user_data` table.
