# Solar Site Monitoring API

The Solar Site Monitoring API is a Flask-based REST API for managing solar-powered telecommunications sites.

The project models a practical monitoring workflow in which teams record site information, solar-panel details, power readings, and operational alerts. It serves as a portfolio reference implementation for backend development and API documentation practices.

> **Project status:** Early development. The application currently provides a health-check endpoint.

***

## Current Functionality

The API currently provides:

* a Flask application factory
* a development server
* a `GET /health` endpoint
* a JSON health-check response

***

## Technology Stack

* Python
* Flask
* Git and GitHub

The project will introduce its database, authentication, validation, testing, documentation, and deployment tools as development continues.

***

## Project Structure

```text
solar-site-monitoring-api/
├── app/
│   └── __init__.py
├── .gitignore
├── README.md
└── requirements.txt
```

The `create_app()` function in `app/__init__.py` creates and configures the Flask application.

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
* OpenAPI documentation and Swagger UI
* automated tests
* Docker support
* background tasks and email notifications
* deployment

Each capability will be added and documented as the API develops.

***

## Project Context

This project draws on experience with solar installations at telecommunications sites in South Africa. It explores how an API could support power monitoring, fault management, and operational reporting.

The application uses simulated project data and does not represent or connect to a production telecommunications system.

***

## Author

**Zamathuli Matseke**<br>
ZainfoDevs
