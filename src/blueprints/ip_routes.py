from flask import Blueprint, jsonify, request

from src.repositories.ip_location_repository import IPLocationRepository

# Create the Blueprint
ip_bp = Blueprint("ip", __name__)


@ip_bp.route("/v1/find-country")
def find_country():
    ip = request.args.get("ip")
    if not ip:
        return jsonify({"error": "IP parameter is missing"}), 400

    # Use repository pattern for database operations
    with IPLocationRepository() as repo:
        result, status_code = repo.find_location_by_ip(ip)

    return jsonify(result), status_code


@ip_bp.route("/v1/stats")
def get_stats():
    """Get database statistics - useful for monitoring"""
    with IPLocationRepository() as repo:
        stats = repo.get_stats()

    return jsonify(stats), 200
