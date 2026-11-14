from datetime import timedelta

from app.extensions import db
from app.models import PowerReading, Site, SolarPanel


def test_site_timestamps_remain_utc_after_database_round_trip(app):
    with app.app_context():
        site = Site(
            site_code="PTA-CBD-001",
            name="Pretoria Central",
            latitude=-25.7479,
            longitude=28.2293,
        )

        db.session.add(site)
        db.session.flush()
        site_id = site.id
        db.session.commit()
        db.session.expunge_all()

        stored_site = db.session.get(Site, site_id)

        assert stored_site is not None
        assert stored_site.created_at.tzinfo is not None
        assert stored_site.created_at.utcoffset() == timedelta(0)
        assert stored_site.updated_at.tzinfo is not None
        assert stored_site.updated_at.utcoffset() == timedelta(0)


def test_solar_panel_timestamps_remain_utc_after_database_round_trip(app):
    with app.app_context():
        site = Site(
            site_code="PTA-CBD-001",
            name="Pretoria Central",
            latitude=-25.7479,
            longitude=28.2293,
        )
        panel = SolarPanel(
            site=site,
            panel_code="SP-101",
            capacity_watts=550.0,
        )

        db.session.add_all([site, panel])
        db.session.flush()
        panel_id = panel.id
        db.session.commit()
        db.session.expunge_all()

        stored_panel = db.session.get(SolarPanel, panel_id)

        assert stored_panel is not None
        assert stored_panel.created_at.tzinfo is not None
        assert stored_panel.created_at.utcoffset() == timedelta(0)
        assert stored_panel.updated_at.tzinfo is not None
        assert stored_panel.updated_at.utcoffset() == timedelta(0)


def test_power_reading_timestamp_remains_utc_after_database_round_trip(app):
    with app.app_context():
        site = Site(
            site_code="PTA-CBD-001",
            name="Pretoria Central",
            latitude=-25.7479,
            longitude=28.2293,
        )

        panel = SolarPanel(
            site=site,
            panel_code="SP-101",
            capacity_watts=550.0,
        )

        reading = PowerReading(
            solar_panel=panel,
            output_watts=350.0,
        )

        db.session.add_all([site, panel, reading])
        db.session.flush()
        reading_id = reading.id
        db.session.commit()
        db.session.expunge_all()

        stored_reading = db.session.get(PowerReading, reading_id)

        assert stored_reading is not None
        assert stored_reading.output_watts == 350.0
        assert stored_reading.solar_panel.panel_code == "SP-101"
        assert stored_reading.recorded_at.tzinfo is not None
        assert stored_reading.recorded_at.utcoffset() == timedelta(0)
