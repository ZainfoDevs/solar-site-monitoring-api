def test_create_power_reading(client):
    site_response = client.post(
        "/sites",
        json={
            "site_code": "PTA-CBD-001",
            "name": "Pretoria Central",
            "latitude": -25.7479,
            "longitude": 28.2293,
        },
    )

    assert site_response.status_code == 201
    site_id = site_response.get_json()["id"]

    panel_response = client.post(
        f"/sites/{site_id}/panels",
        json={
            "panel_code": "SP-101",
            "capacity_watts": 550.0,
        },
    )

    assert panel_response.status_code == 201
    panel_id = panel_response.get_json()["id"]

    response = client.post(
        f"/sites/{site_id}/panels/{panel_id}/readings",
        json={"output_watts": 350.0},
    )

    assert response.status_code == 201

    reading = response.get_json()

    assert isinstance(reading["id"], int)
    assert reading["solar_panel_id"] == panel_id
    assert reading["output_watts"] == 350.0
    assert "recorded_at" in reading


def test_reject_negative_power_reading(client):
    site_response = client.post(
        "/sites",
        json={
            "site_code": "PTA-CBD-001",
            "name": "Pretoria Central",
            "latitude": -25.7479,
            "longitude": 28.2293,
        },
    )

    assert site_response.status_code == 201
    site_id = site_response.get_json()["id"]

    panel_response = client.post(
        f"/sites/{site_id}/panels",
        json={
            "panel_code": "SP-101",
            "capacity_watts": 550.0,
        },
    )

    assert panel_response.status_code == 201
    panel_id = panel_response.get_json()["id"]

    response = client.post(
        f"/sites/{site_id}/panels/{panel_id}/readings",
        json={"output_watts": -50.0},
    )

    assert response.status_code == 422


def test_reject_reading_for_nonexistent_panel(client):
    site_response = client.post(
        "/sites",
        json={
            "site_code": "PTA-CBD-001",
            "name": "Pretoria Central",
            "latitude": -25.7479,
            "longitude": 28.2293,
        },
    )

    assert site_response.status_code == 201
    site_id = site_response.get_json()["id"]

    response = client.post(
        f"/sites/{site_id}/panels/999999/readings",
        json={"output_watts": 350.0},
    )

    assert response.status_code == 404


def test_reject_reading_for_panel_belonging_to_another_site(client):
    site_a_response = client.post(
        "/sites",
        json={
            "site_code": "PTA-CBD-001",
            "name": "Pretoria Central",
            "latitude": -25.7479,
            "longitude": 28.2293,
        },
    )

    assert site_a_response.status_code == 201
    site_a_id = site_a_response.get_json()["id"]

    site_b_response = client.post(
        "/sites",
        json={
            "site_code": "PTA-EAST-002",
            "name": "Pretoria East",
            "latitude": -25.7800,
            "longitude": 28.3000,
        },
    )

    assert site_b_response.status_code == 201
    site_b_id = site_b_response.get_json()["id"]

    panel_response = client.post(
        f"/sites/{site_a_id}/panels",
        json={
            "panel_code": "SP-101",
            "capacity_watts": 550.0,
        },
    )

    assert panel_response.status_code == 201
    panel_id = panel_response.get_json()["id"]

    response = client.post(
        f"/sites/{site_b_id}/panels/{panel_id}/readings",
        json={"output_watts": 350.0},
    )

    assert response.status_code == 404