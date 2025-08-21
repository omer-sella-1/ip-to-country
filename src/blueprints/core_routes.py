from flask import Blueprint, jsonify

# Create the Blueprint
core_bp = Blueprint("core", __name__)


@core_bp.route("/")
def root():
    """Welcome endpoint"""
    return jsonify({"status": "Welcome"})
