from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, DateTime, Float, String
from sqlalchemy.orm import Mapped, mapped_column

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
