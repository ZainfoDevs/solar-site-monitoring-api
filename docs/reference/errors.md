# API Errors

The Solar Site Monitoring API uses HTTP status codes to show whether a request succeeded or failed.

When a request fails, the response body provides information that can help the client identify the problem. The fields included in the response depend on the error type.

## Error Response Fields

An error response may contain the following fields:

| Field | Type | Description |
|---|---|---|
| `code` | integer | HTTP status code returned by the API |
| `status` | string | Standard description of the HTTP status |
| `message` | string | Explanation of the error |
| `errors` | object | Validation errors grouped by request location |

Not every error response includes every field. For example, a `404 Not Found` response may contain only `code` and `status`, while a validation error includes additional details in `errors`.

## 404 Not Found

The API returns `404 Not Found` when a client requests a site that does not exist.

This response can occur when a client tries to:

- retrieve a site
- update a site
- delete a site

For example, the following request asks for site `999`:

```bash
curl -i http://127.0.0.1:5000/sites/999
```

If the database does not contain that site, the API returns:

```json
{
  "code": 404,
  "status": "Not Found"
}
```

Before retrying the request, confirm that the URL contains the correct site `id`. You can use `GET /sites` to view the available site records and their generated identifiers.

## 409 Conflict

The API returns `409 Conflict` when a client tries to create a site with a `site_code` that already belongs to another record.

For example, if `PTA-CBD-001` already exists, the following request fails:

```bash
curl -X POST \
  http://127.0.0.1:5000/sites \
  -H "Content-Type: application/json" \
  -d '{
    "site_code": "PTA-CBD-001",
    "name": "Pretoria Central Backup",
    "latitude": -25.7479,
    "longitude": 28.2293
  }'
```

The API returns an error response similar to:

```json
{
  "code": 409,
  "status": "Conflict",
  "message": "A site with this site code already exists."
}
```

Changing the site name won't resolve the conflict because the API requires each `site_code` to be unique. Use a different operational site code or work with the existing site record.

## 422 Unprocessable Content

The API returns `422 Unprocessable Content` when the request contains data that fails validation.

This error can occur when a client:

- omits a required field
- submits an unsupported site status
- provides a latitude outside the range `-90` to `90`
- provides a longitude outside the range `-180` to `180`
- exceeds the allowed length of a text field

For example, the following request contains an invalid latitude:

```bash
curl -X POST \
  http://127.0.0.1:5000/sites \
  -H "Content-Type: application/json" \
  -d '{
    "site_code": "PTA-CBD-002",
    "name": "Pretoria Central East",
    "latitude": -100,
    "longitude": 28.2293
  }'
```

The API returns a response similar to:

```json
{
  "code": 422,
  "status": "Unprocessable Content",
  "errors": {
    "json": {
      "latitude": [
        "Must be greater than or equal to -90 and less than or equal to 90."
      ]
    }
  }
}
```

The `errors` object identifies the request location, field, and validation rule that caused the failure. Correct the submitted value before resending the request.

## Default Error Response

Swagger UI displays a **Default error response** for each operation. This entry describes the general error structure used when an operation returns an error that is not documented with a specific status code.

`default` is not an HTTP status code. It acts as a fallback in the OpenAPI specification.

The API documents the expected `404`, `409`, and `422` responses separately where they apply. An unexpected error may use the default response structure:

```json
{
  "code": 500,
  "status": "Internal Server Error",
  "message": "An unexpected error occurred."
}
```

Clients should use the numeric value in `code` and the HTTP response status to determine how to handle the failure.

## Error Summary

| Status | Meaning | Applies to |
|---|---|---|
| `404 Not Found` | The requested site does not exist | Retrieve, update, and delete operations |
| `409 Conflict` | Another site already uses the submitted `site_code` | Create operation |
| `422 Unprocessable Content` | The submitted request data failed validation | Create and update operations |
| `500 Internal Server Error` | The API encountered an unexpected problem | Any operation |

## View Errors in Swagger UI

Open Swagger UI at:

```text
http://127.0.0.1:5000/docs
```

Expand an operation to view its documented success and error responses. Select **Try it out** to send a request and inspect the response directly in the browser.

## Next Step

Continue to [Testing](../development/testing.md) to learn how the project verifies its API behavior.
