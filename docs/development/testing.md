# Testing

The project uses `pytest` to test the API before committing or merging changes.

The test suite creates a separate in-memory database for each test. This keeps the development database unchanged and lets every test start from a clean state.

## Test Structure

The tests are stored in the `tests` directory:

```text
tests/
├── conftest.py
├── test_health.py
├── test_site_schemas.py
└── test_sites.py
```

Each file has a specific purpose:

| File | Purpose |
|---|---|
| `conftest.py` | Configures the test application, database, and test client |
| `test_health.py` | Checks the health endpoint |
| `test_site_schemas.py` | Checks site validation and default values |
| `test_sites.py` | Checks the site CRUD operations and their error responses |

The test client sends requests to the Flask application without starting a development server or opening a network connection.

## Run the Tests Locally

Activate the project’s virtual environment before running the tests.

On macOS or Linux:

```bash
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Run the complete test suite from the repository root:

```bash
python -m pytest
```

A successful run should end with output similar to:

```text
12 passed in 0.36s
```

The number of tests and completion time may change as the project develops.

You do not need to start the Flask development server before running the tests. The test client creates and uses the application directly.

## Run Selected Tests

Run one test file when you want to focus on a specific part of the API:

```bash
python -m pytest tests/test_sites.py
```

Run one test function by adding its name after `::`:

```bash
python -m pytest tests/test_sites.py::test_create_site
```

Use the verbose option to display the name and result of each test:

```bash
python -m pytest -v
```

Running a smaller group of tests can provide faster feedback while you work on a specific feature. Run the complete test suite before committing or merging the change.

## Understand the Test Fixtures

The `tests/conftest.py` file defines reusable `pytest` fixtures for the test suite.

The application fixture:

1. creates the Flask application in testing mode
2. configures an in-memory SQLite database
3. creates the database tables before a test runs
4. removes the database session and tables after the test finishes

The client fixture provides a Flask test client:

```python
def test_health_check_returns_ok(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}
```

The `client` fixture sends the request directly to the test application. `pytest` finds the fixture in `conftest.py` and passes it to any test function that includes `client` as a parameter.

This setup keeps the tests independent. A site created in one test does not remain in the database for the next test.

## Run Tests with GitHub Actions

The workflow in `.github/workflows/tests.yml` runs the test suite automatically on an Ubuntu environment.

GitHub Actions starts the workflow when someone:

- pushes a commit to the repository
- opens or updates a pull request

The workflow:

1. checks out the repository
2. installs Python and caches the project dependencies
3. installs the application and development requirements
4. runs `python -m pytest`

Open the repository’s **Actions** tab on GitHub to view the workflow runs. A green check indicates that the automated tests passed. A failed run shows the step and output that caused the failure.

The test-status badge near the top of the repository README shows the result of the latest workflow run.

## Current Test Scope

The current test suite checks:

- the health-check response
- required site fields
- default site status
- coordinate validation
- site creation
- site listing
- single-site retrieval
- partial site updates
- site deletion
- duplicate site-code handling
- missing-site responses

The project will add tests for solar panels, power readings, alerts, authentication, and other resources as those features are implemented.

## Check a Change Before Committing

Run the following checks from the repository root:

```bash
git diff --check
python -m pytest
```

`git diff --check` identifies trailing whitespace and other whitespace errors. `python -m pytest` confirms that the automated tests still pass.

Review the changed files before staging them:

```bash
git diff
git status
```

These checks help catch formatting mistakes, unintended changes, and failing behavior before the code reaches the remote repository.

## Next Step

Continue to [Use Flask-Smorest](../decisions/0001-use-flask-smorest.md) to understand why the project uses Flask-Smorest for request validation and OpenAPI documentation.
