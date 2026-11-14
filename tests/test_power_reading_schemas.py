import pytest
from marshmallow import ValidationError

from app.schemas import PowerReadingCreateSchema


def test_power_reading_create_schema_accepts_zero_output():
    reading_data = {
        "output_watts": 0,
    }

    result = PowerReadingCreateSchema().load(reading_data)

    assert result == {
        "output_watts": 0.0,
    }


def test_power_reading_create_schema_accepts_positive_output():
    reading_data = {
        "output_watts": 350,
    }

    result = PowerReadingCreateSchema().load(reading_data)

    assert result == {
        "output_watts": 350.0,
    }


def test_power_reading_create_schema_rejects_negative_output():
    reading_data = {
        "output_watts": -50,
    }

    with pytest.raises(ValidationError) as error:
        PowerReadingCreateSchema().load(reading_data)

    assert "output_watts" in error.value.messages


def test_power_reading_create_schema_rejects_missing_output():
    reading_data = {}

    with pytest.raises(ValidationError) as error:
        PowerReadingCreateSchema().load(reading_data)

    assert "output_watts" in error.value.messages


def test_power_reading_create_schema_rejects_invalid_output_type():
    reading_data = {
        "output_watts": "unavailable",
    }

    with pytest.raises(ValidationError) as error:
        PowerReadingCreateSchema().load(reading_data)

    assert "output_watts" in error.value.messages