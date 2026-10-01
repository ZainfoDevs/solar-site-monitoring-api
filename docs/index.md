# Solar Site Monitoring API Documentation

Use this documentation to run, explore, and contribute to the Solar Site Monitoring API.

The project models a practical workflow for managing solar-powered mobile network base station sites. At this stage, the API can check its health and create, retrieve, update, and delete site records.

In this documentation, **site** refers to a mobile network base station site.

These pages are intended for developers, contributors, and technical reviewers who want to understand how the API works.

## Where to Begin

If this is your first time working with the project, follow the [Quickstart](quickstart.md). It takes you from installation to your first request.

When the API is running, open the [Swagger UI](http://127.0.0.1:5000/docs) to view the available endpoints and test them in your browser.

For the project overview and software requirements, see the [repository README](../README.md).

## Explore the Documentation

- [Base Station Sites](concepts/sites.md) explains how the API represents a base station site.
- [Manage Sites](guides/manage-sites.md) covers the available site operations.
- [API Errors](reference/errors.md) describes the errors a client may receive.
- [Testing](development/testing.md) explains how to run the test suite and how GitHub Actions checks new changes.
- [Use Flask-Smorest](decisions/0001-use-flask-smorest.md) records the decision to use Flask-Smorest for the API and its OpenAPI documentation.

## What the API Supports Today

The API currently provides:

- a health-check endpoint
- site creation and retrieval
- partial site updates
- site deletion
- request validation
- database migrations
- automated tests
- OpenAPI documentation
- continuous integration through GitHub Actions

## What Comes Later

Future milestones will add solar panels, power readings, operational alerts, authentication, background tasks, and deployment configuration. These features are part of the project roadmap but are not available in the current API.
