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

The API returns `404 Not Found` when a client requests a site that does not exist or a solar panel that does not exist at the specified site.

This response can occur when a client tries to:

- retrieve, update, or delete a site
- list or create solar panels for a site that does not exist
- retrieve, update, or delete a solar panel that does not exist at the specified site

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

When a requested solar panel does not exist at the specified site, the response may also include a message:

```json
{
  "code": 404,
  "message": "The requested solar panel was not found.",
  "status": "Not Found"
}
```

Before retrying the request, confirm that the URL contains the correct site and solar-panel identifiers.

## 409 Conflict

The API returns `409 Conflict` when a request conflicts with an existing resource or relationship.

A conflict can occur when a client:

- creates a site with a `site_code` that already belongs to another site
- creates a solar panel with a `panel_code` that already exists at the same site
- tries to delete a site that still contains solar panels

### Duplicate Site Code

If `PTA-CBD-001` already exists, the API returns:

```json
{
  "code": 409,
  "status": "Conflict",
  "message": "A site with this site code already exists."
}
```

Each `site_code` must be unique. Use a different operational site code or work with the existing site record.

### Duplicate Panel Code

A `panel_code` must be unique within its site. If `SP-101` already exists at the specified site, the API returns:

```json
{
  "code": 409,
  "message": "A solar panel with this panel code already exists at the site.",
  "status": "Conflict"
}
```

You can use the same `panel_code` at a different site.

### Site Contains Solar Panels

You cannot delete a site while solar panels are still associated with it.

The API returns:

```json
{
  "code": 409,
  "message": "Cannot delete a site that still has solar panels.",
  "status": "Conflict"
}
```

Delete the site's solar-panel records before deleting the site.

## 422 Unprocessable Entity

The API returns `422 Unprocessable Entity` when the request contains data that fails validation.

This error can occur when a client:

- omits a required field
- submits an unsupported site or solar-panel status
- provides a latitude outside the range `-90` to `90`
- provides a longitude outside the range `-180` to `180`
- submits a solar-panel capacity that is not greater than `0`
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
  "status": "Unprocessable Entity",
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
  "status": "Internal Server Error"
}
```

Clients should use the numeric value in `code` and the HTTP response status to determine how to handle the failure.

## Error Summary

| Status | Meaning | Applies to |
|---|---|---|
| `404 Not Found` | The requested site or solar panel does not exist | Site and solar-panel operations |
| `409 Conflict` | The request conflicts with an existing identifier or resource relationship | Site creation, solar-panel creation, and site deletion |
| `422 Unprocessable Entity` | The submitted request data failed validation | Create and update operations |
| `500 Internal Server Error` | The API encountered an unexpected problem | Any operation |

## View Errors in Swagger UI

Open Swagger UI at:

```text
http://127.0.0.1:5000/docs
```

Expand an operation to view its documented success and error responses. Select **Try it out** to send a request and inspect the response directly in the browser.

## Next Step

Continue to [Testing](../development/testing.md) to learn how the project verifies its API behavior.
