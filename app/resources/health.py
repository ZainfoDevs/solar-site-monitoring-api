from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import Schema, fields

blp = Blueprint(
    "health",
    __name__,
    description="Application health checks",
)

class HealthResponseSchema(Schema):
    status = fields.String(
        required=True,
        metadata={"description": "Current API status."},
    )

@blp.route("/health")
class HealthCheck(MethodView):
    @blp.response(200, HealthResponseSchema)
    def get(self):
        """Check the API health.

        Confirm that the API is running and can respond to requests.
        """
        return {"status": "ok"}