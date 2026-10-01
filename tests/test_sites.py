def site_payload():
    return {
        "site_code": "PTA-CBD-001",
        "name": "Pretoria Central",
        "latitude": -25.7479,
        "longitude": 28.2293,
    }


def test_create_site(client):
    response = client.post("/sites", json=site_payload())

    assert response.status_code == 201

    site = response.get_json()

    assert site["id"] == 1

    assert site["site_code"] == "PTA-CBD-001"
    assert site["name"] == "Pretoria Central"
    assert site["status"] == "operational"
    assert "created_at" in site
    assert "updated_at" in site


def test_list_sites(client):
    client.post("/sites", json=site_payload())

    response = client.get("/sites")

    assert response.status_code == 200
    assert len(response.get_json()) == 1
    assert response.get_json()[0]["site_code"] == "PTA-CBD-001"


def test_create_site_rejects_duplicate_site_code(client):
    client.post("/sites", json=site_payload())

    response = client.post("/sites", json=site_payload())

    assert response.status_code == 409
    assert response.get_json()["message"] == (
        "A site with this site code already exists."
    )


def test_create_site_rejects_invalid_latitude(client):
    payload = site_payload()
    payload["latitude"] = -100

    response = client.post("/sites", json=payload)

    assert response.status_code == 422


def test_get_site(client):
    created_site = client.post(
        "/sites",
        json=site_payload(),
    ).get_json()

    response = client.get(f"/sites/{created_site['id']}")

    assert response.status_code == 200
    assert response.get_json()["site_code"] == "PTA-CBD-001"


def test_get_site_returns_404_when_site_does_not_exist(client):
    response = client.get("/sites/999")

    assert response.status_code == 404


def test_update_site(client):
    created_site = client.post(
        "/sites",
        json=site_payload(),
    ).get_json()

    response = client.patch(
        f"/sites/{created_site['id']}",
        json={
            "name": "Pretoria Central Rooftop",
            "status": "maintenance",
        },
    )

    assert response.status_code == 200

    updated_site = response.get_json()

    assert updated_site["name"] == "Pretoria Central Rooftop"
    assert updated_site["status"] == "maintenance"
    assert updated_site["site_code"] == "PTA-CBD-001"


def test_delete_site(client):
    created_site = client.post(
        "/sites",
        json=site_payload(),
    ).get_json()

    delete_response = client.delete(
        f"/sites/{created_site['id']}"
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        f"/sites/{created_site['id']}"
    )

    assert get_response.status_code == 404