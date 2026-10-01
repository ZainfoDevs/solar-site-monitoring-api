# ADR 0001: Use Flask-Smorest

- **Status:** Accepted
- **Date:** 2026-09-24

## Context

As the site endpoints took shape, the project needed a consistent way to validate incoming data, format API responses, and generate OpenAPI documentation.

Flask handles application setup and routing, but it doesn’t validate or serialize data against schemas or generate an OpenAPI specification on its own. Managing each concern separately would require describing the same fields in several places. Over time, the code and documentation could easily fall out of step.

The project needed an approach that would keep these parts of the API closely connected while fitting the scale of a small Flask application.

## Decision

The project adopted Flask-Smorest to define the API resources and generate the OpenAPI specification.

Flask-Smorest connects the endpoint definitions with Marshmallow schemas. The schemas describe the data that the API accepts and returns, while Flask-Smorest uses them to:

- validate request data
- serialize response data
- document request and response schemas
- document success and error responses
- generate the OpenAPI specification
- provide interactive API documentation through Swagger UI

The project initializes Flask-Smorest once and registers each resource blueprint with the API. This structure keeps the health and site operations separate while including them in the same OpenAPI document.

## Consequences

### Benefits

- The same schemas support validation, serialization, and API documentation.
- Request validation happens before the endpoint processes the data.
- The generated OpenAPI specification stays close to the implementation.
- Swagger UI gives developers and reviewers a practical way to explore the API.
- Resource blueprints keep the endpoint code organized as the API grows.

### Trade-offs

- The project depends on Flask-Smorest, Marshmallow, Webargs, and APISpec.
- Contributors need to understand Flask-Smorest decorators and Marshmallow schemas.
- The generated documentation is only accurate when developers maintain the schemas, response decorators, and endpoint descriptions.
- Framework-specific decorators make it harder to move the API to another web framework later.

The benefits support the project’s current need for consistent validation and documentation. The added dependencies and framework-specific code are acceptable for the size and purpose of this API.

## Alternatives Considered

### Plain Flask

The project could use Flask routes without an additional API framework. This would keep the dependency list smaller, but the project would need separate code for schema validation, response serialization, and OpenAPI generation.

### Flask-RESTful

Flask-RESTful provides resource-based routing and supports REST API development. However, the project would still need to integrate Marshmallow for validation and add another solution for OpenAPI documentation.

### Manually Maintained OpenAPI Document

The project could keep the API implementation in Flask and write the OpenAPI document separately. This would provide full control over the specification, but every endpoint change would need a matching manual documentation update. The implementation and API contract could drift apart.

Flask-Smorest offered the closest match for the project because it combines Flask resources, Marshmallow schemas, and OpenAPI generation in one workflow.

## Related Implementation

The following files implement this decision:

- [`app/extensions.py`](../../app/extensions.py) creates the shared Flask-Smorest API object.
- [`app/__init__.py`](../../app/__init__.py) configures OpenAPI, initializes the API, and registers the resource blueprints.
- [`app/schemas.py`](../../app/schemas.py) defines the request, response, and error schemas.
- [`app/resources/health.py`](../../app/resources/health.py) documents the health endpoint.
- [`app/resources/sites.py`](../../app/resources/sites.py) defines and documents the site operations.

When the application is running, the generated OpenAPI specification is available at `/openapi.json`, and Swagger UI is available at `/docs`.
