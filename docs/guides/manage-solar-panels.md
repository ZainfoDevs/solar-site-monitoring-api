# Manage Solar Panels

This guide shows you how to create, list, retrieve, update, and delete solar-panel records associated with a mobile network base station site.

The examples use `curl` so that you can send requests from a terminal. You can perform the same operations through Swagger UI at `http://127.0.0.1:5000/docs`.

## Before You Begin

Make sure that you have:

- completed the [Quickstart](../quickstart.md)
- activated the virtual environment
- applied the database migrations
- started the Flask development server
- created at least one base station site

The examples use the following local base address:

```text
http://127.0.0.1:5000
```

Keep the terminal running the Flask server open. Send the requests from a second terminal.

The examples assume that the parent site has an `id` of `1`.

## Create a Solar Panel

Send a `POST` request to `/sites/1/panels` with the panel details:

```bash
curl -X POST \
  http://127.0.0.1:5000/sites/1/panels \
  -H "Content-Type: application/json" \
  -d '{
    "panel_code": "SP-101",
    "capacity_watts": 550.0
  }'
```

The API confirms that the parent site exists, validates the request, creates the panel, and returns a `201 Created` response.

Example response:

```json
{
  "capacity_watts": 550.0,
  "created_at": "2026-10-17T07:00:00.000000",
  "id": 1,
  "panel_code": "SP-101",
  "site_id": 1,
  "status": "operational",
  "updated_at": "2026-10-17T07:00:00.000000"
}
```

The API generates `id`, `site_id`, `created_at`, and `updated_at`.

Because the request does not include `status`, the API assigns `operational`.

Your generated ID and timestamps may differ from the example.

If the specified site does not exist, the API returns a `404 Not Found` response.

A site cannot contain two panels with the same `panel_code`. If the site already contains `SP-101`, the API returns a `409 Conflict` response.

## List Solar Panels for a Site

Send a `GET` request to `/sites/1/panels`:

```bash
curl http://127.0.0.1:5000/sites/1/panels
```

The API returns a `200 OK` response with the site's solar panels, sorted by ascending ID.

Example response:

```json
[
  {
    "capacity_watts": 550.0,
    "created_at": "2026-10-17T07:00:00.000000",
    "id": 1,
    "panel_code": "SP-101",
    "site_id": 1,
    "status": "operational",
    "updated_at": "2026-10-17T07:00:00.000000"
  },
  {
    "capacity_watts": 550.0,
    "created_at": "2026-10-17T07:05:00.000000",
    "id": 2,
    "panel_code": "SP-102",
    "site_id": 1,
    "status": "operational",
    "updated_at": "2026-10-17T07:05:00.000000"
  }
]
```

If the site exists but does not contain any solar-panel records, the API returns an empty list:

```json
[]
```

If the specified site does not exist, the API returns a `404 Not Found` response.

## Retrieve a Solar Panel

Use the generated site and panel IDs to retrieve one solar-panel record:

```bash
curl http://127.0.0.1:5000/sites/1/panels/1
```

The API returns a `200 OK` response when it finds the panel at the specified site.

Example response:

```json
{
  "capacity_watts": 550.0,
  "created_at": "2026-10-17T07:00:00.000000",
  "id": 1,
  "panel_code": "SP-101",
  "site_id": 1,
  "status": "operational",
  "updated_at": "2026-10-17T07:00:00.000000"
}
```

The request must identify both the correct site and the correct panel.

If the panel does not exist at the specified site, the API returns a `404 Not Found` response.

## Update a Solar Panel

Send a `PATCH` request to update selected fields in an existing solar-panel record:

```bash
curl -X PATCH \
  http://127.0.0.1:5000/sites/1/panels/1 \
  -H "Content-Type: application/json" \
  -d '{
    "capacity_watts": 600.0,
    "status": "maintenance"
  }'
```

The API updates only the fields included in the request and returns a `200 OK` response.

Example response:

```json
{
  "capacity_watts": 600.0,
  "created_at": "2026-10-17T07:00:00.000000",
  "id": 1,
  "panel_code": "SP-101",
  "site_id": 1,
  "status": "maintenance",
  "updated_at": "2026-10-17T07:30:00.000000"
}
```

You can update:

- `capacity_watts`
- `status`

The API does not allow clients to change `id`, `site_id`, `panel_code`, `created_at`, or `updated_at`.

The `capacity_watts` value must be greater than zero.

If the panel does not exist at the specified site, the API returns a `404 Not Found` response. If a supplied value fails validation, the API returns a `422 Unprocessable Entity` response.

## Delete a Solar Panel

> **Caution:** Deleting a solar panel permanently removes its record from the current database.

Send a `DELETE` request with the site and panel IDs:

```bash
curl -i -X DELETE http://127.0.0.1:5000/sites/1/panels/1
```

The API deletes the panel and returns a `204 No Content` response. A successful response does not contain a response body.

You can confirm the deletion by requesting the same panel again:

```bash
curl -i http://127.0.0.1:5000/sites/1/panels/1
```

Because the panel no longer exists, the API returns a `404 Not Found` response.

## Delete a Site That Contains Solar Panels

The API does not allow you to delete a site while solar panels are associated with it.

For example:

```bash
curl -i -X DELETE http://127.0.0.1:5000/sites/1
```

If the site still contains one or more panels, the API returns a `409 Conflict` response.

Delete the site's solar-panel records before deleting the site.

This rule prevents solar-panel records from remaining without a valid parent site.

## Response Summary

| Operation | Method and path | Successful response |
|---|---|---|
| Create a panel | `POST /sites/{site_id}/panels` | `201 Created` |
| List panels | `GET /sites/{site_id}/panels` | `200 OK` |
| Retrieve a panel | `GET /sites/{site_id}/panels/{panel_id}` | `200 OK` |
| Update a panel | `PATCH /sites/{site_id}/panels/{panel_id}` | `200 OK` |
| Delete a panel | `DELETE /sites/{site_id}/panels/{panel_id}` | `204 No Content` |

The API may also return:

- `404 Not Found` when the requested site or solar panel does not exist
- `409 Conflict` when the site already contains the submitted `panel_code`
- `409 Conflict` when a client tries to delete a site that still contains solar panels
- `422 Unprocessable Entity` when the request data fails validation

## Next Step

Continue to [API Errors](../reference/errors.md) to learn how the API reports missing resources, conflicts, and invalid request data.
