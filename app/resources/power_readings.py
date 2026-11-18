from flask.views import MethodView
from flask_smorest import Blueprint

from app.extensions import db
from app.models import PowerReading
from app.resources.solar_panels import get_panel_or_404
from app.schemas import (
    ApiErrorSchema,
    PowerReadingCreateSchema,
    PowerReadingSchema,
)


blp = Blueprint(
    "power_readings",
    __name__,
    description="Manage power readings recorded for solar panels.",
)


@blp.route("/sites/<int:site_id>/panels/<int:panel_id>/readings")
class PowerReadingCollection(MethodView):
    @blp.response(
        200,
        PowerReadingSchema(many=True),
        description="Power readings returned successfully.",
    )
    @blp.alt_response(
        404,
        schema=ApiErrorSchema,
        description="The requested solar panel was not found.",
    )
    def get(self, site_id, panel_id):
        """List power readings for a solar panel.

        Return the readings recorded for the specified panel.
        """
        get_panel_or_404(site_id, panel_id)

        return db.session.scalars(
            db.select(PowerReading)
            .where(PowerReading.solar_panel_id == panel_id)
            .order_by(PowerReading.id)
        ).all()

    @blp.arguments(PowerReadingCreateSchema)
    @blp.response(
        201,
        PowerReadingSchema,
        description="Power reading recorded successfully.",
    )
    @blp.alt_response(
        404,
        schema=ApiErrorSchema,
        description="The requested solar panel was not found.",
    )
    @blp.alt_response(
        422,
        schema=ApiErrorSchema,
        description="The request body failed validation.",
    )
    def post(self, reading_data, site_id, panel_id):
        """Record a power reading for a solar panel.

        Validate and store a power measurement for the specified panel.
        """
        get_panel_or_404(site_id, panel_id)

        reading = PowerReading(
            solar_panel_id=panel_id,
            **reading_data,
        )

        db.session.add(reading)
        db.session.commit()

        return reading
