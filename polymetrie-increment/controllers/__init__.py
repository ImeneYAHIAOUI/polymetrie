from flask import Blueprint

from .clients import clients_bp
from .increments import increments_bp

# Enregistrez les blueprints
def register_controllers(app):
    app.register_blueprint(clients_bp)
    app.register_blueprint(increments_bp)