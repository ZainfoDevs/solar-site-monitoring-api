from flask import Flask

from app.extensions import api, db, migrate
from app.models import Site
from app.resources.health import blp as health_blp
from app.resources.sites import blp as sites_blp


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.update(
        API_TITLE="Solar Site Monitoring API",
        API_VERSION="v1",
        OPENAPI_VERSION="3.0.3",
        OPENAPI_URL_PREFIX="/",
        OPENAPI_SWAGGER_UI_PATH="/docs",
        OPENAPI_SWAGGER_UI_URL="https://cdn.jsdelivr.net/npm/swagger-ui-dist/",
        SQLALCHEMY_DATABASE_URI="sqlite:///solar_monitoring.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    api.register_blueprint(health_blp)
    api.register_blueprint(sites_blp)

    return app