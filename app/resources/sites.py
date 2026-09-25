from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import Site
from app.schemas import SiteCreateSchema, SiteSchema, SiteUpdateSchema

blp = Blueprint(
    "sites",
    __name__,
    description="Telecommunications site operations",
)


@blp.route("/sites")
class SiteCollection(MethodView):
    @blp.response(200, SiteSchema(many=True))
    def get(self):
        """List telecommunications sites.

        Return all sites in ascending identifier order.
        """
        return db.session.scalars(
            db.select(Site).order_by(Site.id)
        ).all()

    @blp.arguments(SiteCreateSchema)
    @blp.response(201, SiteSchema)
    def post(self, site_data):
        """Create a telecommunications site.

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
    @blp.response(200, SiteSchema)
    def get(self, site_id):
        """Retrieve a telecommunications site.

        Return the site identified by its database identifier.
        """
        return db.get_or_404(Site, site_id)

    @blp.arguments(SiteUpdateSchema)
    @blp.response(200, SiteSchema)
    def patch(self, site_data, site_id):
        """Update a telecommunications site.

        Update the supplied fields for an existing site.
        """
        site = db.get_or_404(Site, site_id)

        for field, value in site_data.items():
            setattr(site, field, value)

        db.session.commit()

        return site

    @blp.response(204)
    def delete(self, site_id):
        """Delete a telecommunications site.

        Remove the site identified by its database identifier.
        """
        site = db.get_or_404(Site, site_id)

        db.session.delete(site)
        db.session.commit()