from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import Site
from app.schemas import (
    ApiErrorSchema,
    SiteCreateSchema,
    SiteSchema,
    SiteUpdateSchema,
)


blp = Blueprint(
    "sites",
    __name__,
    description="Manage mobile network base station sites.",
)


@blp.route("/sites")
class SiteCollection(MethodView):
    @blp.response(
        200,
        SiteSchema(many=True),
        description="Sites returned successfully.",
    )
    def get(self):
        """List mobile network base station sites.

        Return all sites in ascending identifier order.
        """
        return db.session.scalars(
            db.select(Site).order_by(Site.id)
        ).all()

    @blp.arguments(SiteCreateSchema)
    @blp.response(
        201,
        SiteSchema,
        description="Site created successfully.",
    )
    @blp.alt_response(
        409,
        schema=ApiErrorSchema,
        description="A site with the same site code already exists.",
    )
    @blp.alt_response(
        422,
        schema=ApiErrorSchema,
        description="The request body failed validation.",
    )
    def post(self, site_data):
        """Create a mobile network base station site.

        Validate and store a new site.
        """
        site = Site(**site_data)
        db.session.add(site)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(
                409,
                message="A site with this site code already exists.",
            )

        return site


@blp.route("/sites/<int:site_id>")
class SiteDetail(MethodView):
    @blp.response(
        200,
        SiteSchema,
        description="Site returned successfully.",
    )
    @blp.alt_response(
        404,
        schema=ApiErrorSchema,
        description="The requested site was not found.",
    )
    def get(self, site_id):
        """Retrieve a mobile network base station site..

        Return the site identified by its database identifier.
        """
        return db.get_or_404(Site, site_id)

    @blp.arguments(SiteUpdateSchema)
    @blp.response(
        200,
        SiteSchema,
        description="Site updated successfully.",
    )
    @blp.alt_response(
        404,
        schema=ApiErrorSchema,
        description="The requested site was not found.",
    )
    @blp.alt_response(
        422,
        schema=ApiErrorSchema,
        description="The request body failed validation.",
    )
    def patch(self, site_data, site_id):
        """Update a mobile network base station site.

        Update the supplied fields for an existing site.
        """
        site = db.get_or_404(Site, site_id)

        for field, value in site_data.items():
            setattr(site, field, value)

        db.session.commit()

        return site

    @blp.response(
        204,
        description="Site deleted successfully.",
    )
    @blp.alt_response(
        404,
        schema=ApiErrorSchema,
        description="The requested site was not found.",
    )
    def delete(self, site_id):
        """"Delete a mobile network base station site.

        Remove the site identified by its database identifier.
        """
        site = db.get_or_404(Site, site_id)

        db.session.delete(site)
        db.session.commit()