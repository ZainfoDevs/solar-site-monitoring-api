# Solar Site Monitoring API

The Solar Site Monitoring API is a Flask-based REST API for managing solar-powered telecommunications sites.

The project models a practical monitoring workflow in which teams record site information, solar-panel details, power readings, and operational alerts. It serves as a portfolio reference implementation for backend development and API documentation practices.

> **Project status:** Early development. The application currently provides a documented health-check endpoint and an automated endpoint test.

***

## Current Functionality

The API currently provides:

* a Flask application factory
* Flask-Smorest blueprint-based routing
* a `GET /health` endpoint
* generated OpenAPI documentation
* Swagger UI
* an automated health-endpoint test with pytest

***

## Technology Stack

* Python
* Flask
* Flask-Smorest
* Marshmallow
* OpenAPI and Swagger UI
* pytest
* Git and GitHub

The project will introduce its database, authentication, deployment, and additional testing tools as development continues.

***

## Project Structure

solar-site-monitoring-api/
├── app/
│   ├── resources/
│   │   ├── __init__.py
│   │   └── health.py
│   ├── __init__.py
│   └── extensions.py
├── tests/
│   ├── conftest.py
│   └── test_health.py
├── .gitignore
├── LICENSE
├── README.md
├── requirements-dev.txt
└── requirements.txt

***

## Prerequisites

Before running the project, install:

* Python 3
* Git

You also need a terminal or command-line application.

***

## Set Up the Project

Clone the repository:

```bash
git clone https://github.com/ZainfoDevs/solar-site-monitoring-api.git
```

Open the project directory:

```bash
cd solar-site-monitoring-api
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate the environment on macOS or Linux:

```bash
source .venv/bin/activate
```

On Windows PowerShell, run:

```powershell
.venv\Scripts\Activate.ps1
```

Install the project dependencies:

```bash
python -m pip install -r requirements.txt
```

To install the runtime dependencies together with development and testing tools, run:

```bash
python -m pip install -r requirements-dev.txt
```

***

## Run the API

Start the Flask development server:

```bash
python -m flask --app app:create_app run --debug
```

Flask runs the API at:

```text
http://127.0.0.1:5000
```

> **Note:** Flask's development server is suitable for local development only. Do not use it in a production deployment.

***

## Test the Health Endpoint

Send a request to the health endpoint:

```bash
curl -i http://127.0.0.1:5000/health
```

A successful request returns an HTTP `200 OK` status and the following JSON response:

```json
{
  "status": "ok"
}
```

The health endpoint confirms that the application is running and can respond to requests.

***

## Run the Automated Tests

Install the development dependencies, then run:

```bash
python -m pytest
```

A successful test run confirms that the health endpoint returns `200 OK` and the expected JSON response.

***

## Planned Development

The project roadmap includes:

* telecommunications site management
* solar-panel records
* power-reading collection
* operational alerts
* request validation
* SQLAlchemy database models
* database migrations with Alembic and Flask-Migrate
* JWT authentication and authorization
* expanded automated test coverage
* Docker support
* background tasks and email notifications
* deployment

Each capability will be added and documented as the API develops.

***

## Project Context

This project draws on experience with solar installations at telecommunications sites in South Africa. It explores how an API could support power monitoring, fault management, and operational reporting.

The application uses simulated project data and does not represent or connect to a production telecommunications system.

***

## License

This project is licensed under the [MIT License](LICENSE).

***

## Author

**Zamathuli Matseke**<br>
ZainfoDevs
