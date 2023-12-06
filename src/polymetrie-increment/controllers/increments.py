from flask import Blueprint, request
from services import *
from service import app
import time
import psutil

http_calls_counter, request_duration_histogram, memory_usage_gauge, cpu_time_gauge = app.config["prometheus_metrics"]

increments_bp = Blueprint('increments', __name__)

@increments_bp.route("/api/client/increment", methods=["POST"])
def create_increment():
    http_calls_counter.inc()
    start_time = time.time()

    # Request data
    data = request.get_json()
    url = data["url"]
    
    # Increment the counter for the client
    add_increment(url)    

    # Prometheus metrics
    duration = time.time() - start_time
    request_duration_histogram.observe(duration)

    # Get real hardware metrics using psutil
    memory_usage_gauge.observe(psutil.virtual_memory().used)
    cpu_time_gauge.observe(psutil.cpu_percent() / 100.0)
    
    return "OK";

@increments_bp.route("/api/client/increment", methods=["GET"])
def get_all_increments():
    return query_all_increments()