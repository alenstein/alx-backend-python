# 0x03. Unittests and Integration Tests

This project focuses on learning and applying the principles of unit and integration testing in Python. The primary goal is to understand the distinction between these two types of tests and to implement common testing patterns such as mocking, parameterization, and fixtures.

## Project Structure

The project is composed of several files, each serving a specific purpose in the testing process:

*   `utils.py`: A module containing utility functions (`access_nested_map`, `get_json`, and `memoize`) that are the subject of our unit tests.
*   `client.py`: This module features the `GithubOrgClient` class, designed to interact with the GitHub API. It serves as the basis for both unit and integration testing exercises.
*   `test_utils.py`: This file houses the unit tests for the functions defined in `utils.py`. It employs techniques like parameterization with `parameterized` and mocking with `unittest.mock` to ensure the utility functions behave as expected under various conditions.
*   `test_client.py`: Contains the test suite for the `GithubOrgClient` class. This includes unit tests that mock external dependencies and integration tests that use fixtures to simulate the interaction with the GitHub API, verifying the end-to-end behavior of the client.
*   `fixtures.py`: Provides a set of test fixtures, which are pre-defined data payloads that mimic the responses from the GitHub API. These fixtures are crucial for creating realistic and repeatable integration tests without making actual network requests.

## Learning Objectives

Through this project, we gain a practical understanding of:

*   **Unit Testing**: Isolating and testing individual functions and methods to verify their correctness.
*   **Integration Testing**: Testing the interaction between different parts of the application to ensure they work together as intended.
*   **Mocking**: Replacing external dependencies and complex objects with mock objects to create controlled test environments.
*   **Parameterization**: Running the same test with different sets of inputs to cover a wider range of scenarios.
*   **Fixtures**: Using static data sets to ensure consistent and predictable test outcomes.

## How to Run Tests

To execute the tests, you can use Python's built-in `unittest` module from the command line. Navigate to the project's root directory and run the following command for a specific test file:

```bash
python -m unittest 0x03-Unittests_and_integration_tests/test_client.py
```

Replace `test_client.py` with the name of the test file you wish to run.
