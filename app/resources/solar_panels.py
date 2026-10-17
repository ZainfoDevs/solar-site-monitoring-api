from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import Site, SolarPanel
from app.schemas import (
    ApiErrorSchema,
    SolarPanelCreateSchema,
    SolarPanelSchema,
    SolarPanelUpdateSchema,
)


blp = Blueprint(
    "solar_panels",
    __name__,
    description="Manage solar panels installed at base station sites.",
)


def get_panel_or_404(site_id, panel_id):
    panel = db.session.scalar(
        db.select(SolarPanel).where(
            SolarPanel.id == panel_id,
            SolarPanel.site_id == site_id,
        )
    )

    if panel is None:
        abort(
            404,
            message="The requested solar panel was not found.",
        )

    return panel


@blp.route("/sites/<int:site_id>/panels")
class SolarPanelCollection(MethodView):
    @blp.response(
        200,
        SolarPanelSchema(many=True),
        description="Solar panels returned successfully.",
    )
    @blp.alt_response(
        404,
        schema=ApiErrorSchema,
        description="The requested site was not found.",
    )
    def get(self, site_id):
        """List solar panels for a site.

        Return the solar panels installed at the specified site.
        """
        db.get_or_404(Site, site_id)

        return db.session.scalars(
            db.select(SolarPanel)
            .where(SolarPanel.site_id == site_id)
            .order_by(SolarPanel.id)
        ).all()

    @blp.arguments(SolarPanelCreateSchema)
    @blp.response(
        201,
        SolarPanelSchema,
        description="Solar panel created successfully.",
    )
    @blp.alt_response(
        404,
        schema=ApiErrorSchema,
        description="The requested site was not found.",
    )
    @blp.alt_response(
        409,
        schema=ApiErrorSchema,
        description="The site already contains a panel with this panel code.",
    )
    @blp.alt_response(
        422,
        schema=ApiErrorSchema,
        description="The request body failed validation.",
    )
    def post(self, panel_data, site_id):
        """Create a solar panel for a site.

        Validate and store a new solar panel at the specified site.
        """
        db.get_or_404(Site, site_id)

        panel = SolarPanel(
            site_id=site_id,
            **panel_data,
        )
        db.session.add(panel)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(
                409,
                message=(
                    "A solar panel with this panel code already "
                    "exists at the site."
                ),
            )

        return panel


@blp.route("/sites/<int:site_id>/panels/<int:panel_id>")
class SolarPanelDetail(MethodView):
    @blp.response(
        200,
        SolarPanelSchema,
        description="Solar panel returned successfully.",
    )
    @blp.alt_response(
        404,
        schema=ApiErrorSchema,
        description="The requested solar panel was not found.",
    )
    def get(self, site_id, panel_id):
        """Retrieve a solar panel.

        Return a solar panel installed at the specified site.
        """
        return get_panel_or_404(site_id, panel_id)

    @blp.arguments(SolarPanelUpdateSchema)
    @blp.response(
        200,
        SolarPanelSchema,
        description="Solar panel updated successfully.",
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
    def patch(self, panel_data, site_id, panel_id):
        """Update a solar panel.

        Update the supplied fields for an existing solar panel.
        """
        panel = get_panel_or_404(site_id, panel_id)

        for field, value in panel_data.items():
            setattr(panel, field, value)

        db.session.commit()

        return panel

    @blp.response(
        204,
        description="Solar panel deleted successfully.",
    )
    @blp.alt_response(
        404,
        schema=ApiErrorSchema,
        description="The requested solar panel was not found.",
    )
    def delete(self, site_id, panel_id):
        """Delete a solar panel.

        Remove a solar panel from the specified site.
        """
        panel = get_panel_or_404(site_id, panel_id)

        db.session.delete(panel)
        db.session.commit()
