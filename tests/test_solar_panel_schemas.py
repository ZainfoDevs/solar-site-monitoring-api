import pytest
from marshmallow import ValidationError

from app.schemas import SolarPanelCreateSchema


def test_solar_panel_create_schema_loads_valid_panel():
    panel_data = {
        "panel_code": "SP-101",
        "capacity_watts": 550.0,
    }

    result = SolarPanelCreateSchema().load(panel_data)

    assert result == {
        "panel_code": "SP-101",
        "capacity_watts": 550.0,
        "status": "operational",
    }


def test_solar_panel_create_schema_rejects_non_positive_capacity():
    panel_data = {
        "panel_code": "SP-101",
        "capacity_watts": 0,
    }

    with pytest.raises(ValidationError) as error:
        SolarPanelCreateSchema().load(panel_data)

    assert "capacity_watts" in error.value.messages


def test_solar_panel_create_schema_rejects_unsupported_status():
    panel_data = {
        "panel_code": "SP-101",
        "capacity_watts": 550.0,
        "status": "unknown",
    }

    with pytest.raises(ValidationError) as error:
        SolarPanelCreateSchema().load(panel_data)

    assert "status" in error.value.messages
