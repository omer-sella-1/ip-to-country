from flask import Flask, jsonify, request

from src.blueprints.core_routes import core_bp
from src.blueprints.ip_routes import ip_bp
from src.config import Config
from src.services.rate_limiter import RateLimiter


def create_app() -> Flask:
    app = Flask(__name__)

    app.json.sort_keys = False

    rate_limiter = RateLimiter()

    @app.before_request
    def check_rate_limit():
        client_ip = request.remote_addr
        if not rate_limiter.is_allowed(client_ip, Config.RATE_LIMIT_PER_SECOND):
            return jsonify({"error": "Rate limit exceeded"}), 429
        return None

    app.register_blueprint(core_bp)
    app.register_blueprint(ip_bp)

    return app
