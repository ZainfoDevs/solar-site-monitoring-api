from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


class Site(db.Model):
    __tablename__ = "sites"
    __table_args__ = (
        CheckConstraint(
            "latitude BETWEEN -90 AND 90",
            name="ck_sites_latitude_range",
        ),
        CheckConstraint(
            "longitude BETWEEN -180 AND 180",
            name="ck_sites_longitude_range",
        ),
        CheckConstraint(
            "status IN ('operational', 'maintenance', 'offline')",
            name="ck_sites_status",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    site_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    latitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    longitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        default="operational",
        server_default="operational",
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    solar_panels: Mapped[list["SolarPanel"]] = relationship(
        back_populates="site",
    )


class SolarPanel(db.Model):
    __tablename__ = "solar_panels"
    __table_args__ = (
        CheckConstraint(
            "capacity_watts > 0",
            name="ck_solar_panels_capacity_positive",
        ),
        CheckConstraint(
            "status IN ('operational', 'maintenance', 'offline')",
            name="ck_solar_panels_status",
        ),
        UniqueConstraint(
            "site_id",
            "panel_code",
            name="uq_solar_panels_site_panel_code",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    site_id: Mapped[int] = mapped_column(
        ForeignKey("sites.id"),
        index=True,
        nullable=False,
    )
    panel_code: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    capacity_watts: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        default="operational",
        server_default="operational",
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    site: Mapped[Site] = relationship(
        back_populates="solar_panels",
    )
