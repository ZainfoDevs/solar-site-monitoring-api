# Manage Base Station Sites

This guide shows you how to create, list, retrieve, update, and delete mobile network base station site records.

The examples use `curl` so that you can send requests from a terminal. You can perform the same operations through Swagger UI at `http://127.0.0.1:5000/docs`.

## Before You Begin

Make sure that you have:

- completed the [Quickstart](../quickstart.md)
- activated the virtual environment
- applied the database migrations
- started the Flask development server

The examples use the following local base address:

```text
http://127.0.0.1:5000
```

Keep the terminal running the Flask server open. Send the requests from a second terminal.

## Create a Site

Send a `POST` request to `/sites` with the site details:

```bash
curl -X POST \
  http://127.0.0.1:5000/sites \
  -H "Content-Type: application/json" \
  -d '{
    "site_code": "PTA-CBD-001",
    "name": "Pretoria Central",
    "latitude": -25.7479,
    "longitude": 28.2293
  }'
```

The API validates the request, creates the site, and returns a `201 Created` response.

Example response:

```json
{
  "created_at": "2026-09-30T12:00:00.000000",
  "id": 1,
  "latitude": -25.7479,
  "longitude": 28.2293,
  "name": "Pretoria Central",
  "site_code": "PTA-CBD-001",
  "status": "operational",
  "updated_at": "2026-09-30T12:00:00.000000"
}
```

The API generates `id`, `created_at`, and `updated_at`. Because the request does not include `status`, the API assigns `operational`.

Your generated ID and timestamps may differ from the example.

## List the Sites

Send a `GET` request to `/sites`:

```bash
curl http://127.0.0.1:5000/sites
```

The API returns a `200 OK` response containing the available sites in ascending ID order.

Example response:

```json
[
  {
    "created_at": "2026-09-30T12:00:00.000000",
    "id": 1,
    "latitude": -25.7479,
    "longitude": 28.2293,
    "name": "Pretoria Central",
    "site_code": "PTA-CBD-001",
    "status": "operational",
    "updated_at": "2026-09-30T12:00:00.000000"
  }
]
```

If the database does not contain any site records, the API returns an empty list:

```json
[]
```

## Retrieve a Site

Use the site’s generated `id` to retrieve one site record:

```bash
curl http://127.0.0.1:5000/sites/1
```

The API returns a `200 OK` response when it finds the site.

Example response:

```json
{
  "created_at": "2026-09-30T12:00:00.000000",
  "id": 1,
  "latitude": -25.7479,
  "longitude": 28.2293,
  "name": "Pretoria Central",
  "site_code": "PTA-CBD-001",
  "status": "operational",
  "updated_at": "2026-09-30T12:00:00.000000"
}
```

Replace `1` in the request path with the `id` of the site you want to retrieve.

If the specified site does not exist, the API returns a `404 Not Found` response:

```json
{
  "code": 404,
  "status": "Not Found"
}
```
## Update a Site

Send a `PATCH` request to update selected fields in an existing site record:

```bash
curl -X PATCH \
  http://127.0.0.1:5000/sites/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Pretoria Central Rooftop",
    "status": "maintenance"
  }'
```

The API updates only the fields included in the request and returns a `200 OK` response.

Example response:

```json
{
  "created_at": "2026-09-30T12:00:00.000000",
  "id": 1,
  "latitude": -25.7479,
  "longitude": 28.2293,
  "name": "Pretoria Central Rooftop",
  "site_code": "PTA-CBD-001",
  "status": "maintenance",
  "updated_at": "2026-09-30T12:30:00.000000"
}
```

You can update the following fields:

- `name`
- `latitude`
- `longitude`
- `status`

The API does not allow clients to change `id`, `site_code`, `created_at`, or `updated_at`.

If the site does not exist, the API returns a `404 Not Found` response. If a supplied value fails validation, it returns a `422 Unprocessable Content` response.

## Delete a Site

> **Caution:** Deleting a site permanently removes its record from the current database.

Send a `DELETE` request with the site’s generated `id`:

```bash
curl -i -X DELETE http://127.0.0.1:5000/sites/1
```

The API deletes the site and returns a `204 No Content` response. A successful response does not contain a response body.

You can confirm the deletion by requesting the same site again:

```bash
curl -i http://127.0.0.1:5000/sites/1
```

Because the record no longer exists, the API returns a `404 Not Found` response.

If the site does not exist when you send the `DELETE` request, the API also returns a `404 Not Found`.

## Response Summary

| Operation | Method and path | Successful response |
|---|---|---|
| Create a site | `POST /sites` | `201 Created` |
| List sites | `GET /sites` | `200 OK` |
| Retrieve a site | `GET /sites/{site_id}` | `200 OK` |
| Update a site | `PATCH /sites/{site_id}` | `200 OK` |
| Delete a site | `DELETE /sites/{site_id}` | `204 No Content` |

The API may also return:

- `404 Not Found` when the requested site does not exist
- `409 Conflict` when another site already uses the submitted `site_code`
- `422 Unprocessable Content` when the request data fails validation

## Next Step

Continue to [API Errors](../reference/errors.md) to learn how the API reports missing resources, duplicate site codes, and invalid request data.
