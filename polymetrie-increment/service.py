# Prometheus
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
import random 
import psutil

# Metrics
http_calls_counter = Counter('http_calls_total', 'Total number of HTTP calls')
request_duration_histogram = Histogram('request_duration_seconds', 'Request duration in seconds')
memory_usage_gauge = Histogram('memory_usage_bytes', 'Memory usage in bytes')
cpu_time_gauge = Histogram('cpu_time_seconds', 'CPU time consumed in seconds')

# Flask
from flask import Flask, request, jsonify, Response
import os
app = Flask(__name__)


app.config["prometheus_metrics"] = [http_calls_counter, request_duration_histogram, memory_usage_gauge, cpu_time_gauge]

# set DB
from models import register_models
register_models(app)

# Set Controllers
from controllers import register_controllers
register_controllers(app)


@app.route("/metrics", methods=["GET"])
def metrics():
    return Response(generate_latest(), content_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")