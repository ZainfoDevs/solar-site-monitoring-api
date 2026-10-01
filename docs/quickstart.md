# Quickstart

This guide takes you from cloning the project to sending your first API request.

## Prerequisites

Before you begin, make sure you have:

- Git
- Python 3.14
- access to a terminal

The project uses SQLite for local development, so you don't need to install a separate database server.

## Clone the Repository

Clone the repository and move into the project directory:

```bash
git clone https://github.com/ZainfoDevs/solar-site-monitoring-api.git
cd solar-site-monitoring-api
```

## Create a Virtual Environment

Create a virtual environment to keep the project dependencies separate from other Python installations.

On macOS or Linux, run:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell, run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

After activation, the terminal prompt should begin with `(.venv)`.

## Install the Dependencies

Upgrade `pip` inside the virtual environment:

```bash
python -m pip install --upgrade pip
```

Install the application and development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

The development requirements include the packages needed to run the API and its automated tests.

## Prepare the Database

Apply the database migrations:

```bash
python -m flask --app app:create_app db upgrade
```

This command creates the local SQLite database if it does not exist and applies the latest database structure.

## Start the API

Run the Flask development server:

```bash
python -m flask --app app:create_app run --debug
```

The API starts at:

```text
http://127.0.0.1:5000
```

The command runs the API in the terminal. It does not automatically open a browser. Keep this terminal open while you work with the API.

> **Note:** The Flask development server is intended for local development. Do not use it in a production environment.

## Send Your First Request

Keep the Flask server running and open a second terminal.

On macOS or Linux, send a request to the health endpoint:

```bash
curl http://127.0.0.1:5000/health
```

On Windows PowerShell, run:

```powershell
curl.exe http://127.0.0.1:5000/health
```

The API should return:

```json
{
  "status": "ok"
}
```

This response confirms that the API is running and can respond to requests.

## Explore the API

Open Google Chrome, Mozilla Firefox, Safari, Microsoft Edge, or another web browser. Enter the following address:

```text
http://127.0.0.1:5000/docs
```

`http://127.0.0.1:5000` is the local base address. Adding `/docs` opens Swagger UI.

Expand the **sites** section to view the available site endpoints. Swagger UI shows the request fields, response fields, status codes, and documented errors for each operation.

Select **Try it out** to send a request from the browser.

## Stop the API

Return to the terminal running the Flask server and press `Control+C`.

## Run the Tests

Run the automated test suite:

```bash
python -m pytest
```

A successful test run confirms that the health check, site schemas, and site operations behave as expected.

## Next Step

Continue to [Manage Sites](guides/manage-sites.md) to create, retrieve, update, and delete base station site records.
