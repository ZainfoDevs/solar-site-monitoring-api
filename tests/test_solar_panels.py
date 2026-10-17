def site_payload(site_code="PTA-CBD-001"):
    return {
        "site_code": site_code,
        "name": "Pretoria Central",
        "latitude": -25.7479,
        "longitude": 28.2293,
    }


def panel_payload(panel_code="SP-101"):
    return {
        "panel_code": panel_code,
        "capacity_watts": 550.0,
    }


def create_site(client, site_code="PTA-CBD-001"):
    return client.post(
        "/sites",
        json=site_payload(site_code),
    ).get_json()


def test_create_solar_panel(client):
    site = create_site(client)

    response = client.post(
        f"/sites/{site['id']}/panels",
        json=panel_payload(),
    )

    assert response.status_code == 201

    panel = response.get_json()

    assert panel["id"] == 1
    assert panel["site_id"] == site["id"]
    assert panel["panel_code"] == "SP-101"
    assert panel["capacity_watts"] == 550.0
    assert panel["status"] == "operational"
    assert "created_at" in panel
    assert "updated_at" in panel


def test_list_solar_panels_for_site(client):
    site = create_site(client)

    client.post(
        f"/sites/{site['id']}/panels",
        json=panel_payload("SP-101"),
    )
    client.post(
        f"/sites/{site['id']}/panels",
        json=panel_payload("SP-102"),
    )

    response = client.get(
        f"/sites/{site['id']}/panels"
    )

    assert response.status_code == 200

    panels = response.get_json()

    assert len(panels) == 2
    assert panels[0]["panel_code"] == "SP-101"
    assert panels[1]["panel_code"] == "SP-102"


def test_create_solar_panel_returns_404_when_site_does_not_exist(client):
    response = client.post(
        "/sites/999/panels",
        json=panel_payload(),
    )

    assert response.status_code == 404


def test_create_solar_panel_rejects_duplicate_panel_code_at_same_site(client):
    site = create_site(client)

    client.post(
        f"/sites/{site['id']}/panels",
        json=panel_payload(),
    )

    response = client.post(
        f"/sites/{site['id']}/panels",
        json=panel_payload(),
    )

    assert response.status_code == 409
    assert response.get_json()["message"] == (
        "A solar panel with this panel code already exists at the site."
    )


def test_same_panel_code_can_exist_at_different_sites(client):
    first_site = create_site(client, "PTA-CBD-001")
    second_site = create_site(client, "PTA-CBD-002")

    first_response = client.post(
        f"/sites/{first_site['id']}/panels",
        json=panel_payload(),
    )
    second_response = client.post(
        f"/sites/{second_site['id']}/panels",
        json=panel_payload(),
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 201


def test_get_solar_panel(client):
    site = create_site(client)

    panel = client.post(
        f"/sites/{site['id']}/panels",
        json=panel_payload(),
    ).get_json()

    response = client.get(
        f"/sites/{site['id']}/panels/{panel['id']}"
    )

    assert response.status_code == 200
    assert response.get_json()["panel_code"] == "SP-101"


def test_get_solar_panel_returns_404_for_wrong_site(client):
    first_site = create_site(client, "PTA-CBD-001")
    second_site = create_site(client, "PTA-CBD-002")

    panel = client.post(
        f"/sites/{first_site['id']}/panels",
        json=panel_payload(),
    ).get_json()

    response = client.get(
        f"/sites/{second_site['id']}/panels/{panel['id']}"
    )

    assert response.status_code == 404


def test_update_solar_panel(client):
    site = create_site(client)

    panel = client.post(
        f"/sites/{site['id']}/panels",
        json=panel_payload(),
    ).get_json()

    response = client.patch(
        f"/sites/{site['id']}/panels/{panel['id']}",
        json={
            "capacity_watts": 600.0,
            "status": "maintenance",
        },
    )

    assert response.status_code == 200

    updated_panel = response.get_json()

    assert updated_panel["capacity_watts"] == 600.0
    assert updated_panel["status"] == "maintenance"
    assert updated_panel["panel_code"] == "SP-101"
    assert updated_panel["site_id"] == site["id"]


def test_delete_solar_panel(client):
    site = create_site(client)

    panel = client.post(
        f"/sites/{site['id']}/panels",
        json=panel_payload(),
    ).get_json()

    delete_response = client.delete(
        f"/sites/{site['id']}/panels/{panel['id']}"
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        f"/sites/{site['id']}/panels/{panel['id']}"
    )

    assert get_response.status_code == 404

def test_delete_site_rejected_when_site_has_solar_panels(client):
    site = create_site(client)

    client.post(
        f"/sites/{site['id']}/panels",
        json=panel_payload(),
    )

    response = client.delete(
        f"/sites/{site['id']}"
    )

    assert response.status_code == 409
    assert response.get_json()["message"] == (
        "Cannot delete a site that still has solar panels."
    )