from flask import Flask


def create_app():
    app = Flask(__name__)

    @app.get("/health")
    def health_check():
        return {"status": "ok"}, 200

    return app
