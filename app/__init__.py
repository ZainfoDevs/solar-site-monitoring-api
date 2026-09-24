from flask import Flask

from app.extensions import api
from app.resources.health import blp as health_blp


def create_app():
    app = Flask(__name__)

    app.config.update(
        API_TITLE="Solar Site Monitoring API",
        API_VERSION="v1",
        OPENAPI_VERSION="3.0.3",
        OPENAPI_URL_PREFIX="/",
        OPENAPI_SWAGGER_UI_PATH="/docs",
        OPENAPI_SWAGGER_UI_URL="https://cdn.jsdelivr.net/npm/swagger-ui-dist/",
    )

    api.init_app(app)
    api.register_blueprint(health_blp)

    return app