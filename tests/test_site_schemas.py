import pytest
from marshmallow import ValidationError

from app.schemas import SiteCreateSchema


def test_site_create_schema_loads_valid_site():
    site_data = {
        "site_code": "PTA-CBD-001",
        "name": "Pretoria Central",
        "latitude": -25.7479,
        "longitude": 28.2293,
    }

    result = SiteCreateSchema().load(site_data)

    assert result == {
        "site_code": "PTA-CBD-001",
        "name": "Pretoria Central",
        "latitude": -25.7479,
        "longitude": 28.2293,
        "status": "operational",
    }


def test_site_create_schema_rejects_invalid_latitude():
    site_data = {
        "site_code": "PTA-CBD-001",
        "name": "Pretoria Central",
        "latitude": -100,
        "longitude": 28.2293,
    }

    with pytest.raises(ValidationError) as error:
        SiteCreateSchema().load(site_data)

    assert "latitude" in error.value.messages


def test_site_create_schema_rejects_unsupported_status():
    site_data = {
        "site_code": "PTA-CBD-001",
        "name": "Pretoria Central",
        "latitude": -25.7479,
        "longitude": 28.2293,
        "status": "unknown",
    }

    with pytest.raises(ValidationError) as error:
        SiteCreateSchema().load(site_data)

    assert "status" in error.value.messages
