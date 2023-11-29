from flask import Blueprint, request
from services import *

clients_bp = Blueprint('clients', __name__)

@clients_bp.route("/api/client", methods=["POST"])
def create_user():
    data = request.get_json()
    name, url, email, phone = data["name"], data["url"], data["email"], data["phone"]
    try:
        return add_client(name, url, email, phone), 201
    except Exception as e:
        print(f"The error '{e}' occurred.")
        return {"error": "An error occurred while creating the user."}, 500

@clients_bp.route("/api/client/default", methods=["POST"])
def create_default_client():
    # create client in postgres
    print("create client in postgres")
    return add_client("Default", "https://www.google.com", "default@localhost", "0000000000"),201

@clients_bp.route("/api/client", methods=["GET"])
def get_all_users():
    try:
        return query_all_clients()
    except Exception as e:
        print(f"The error '{e}' occurred.")
        return {"error": "An error occurred while getting all users."}, 500

