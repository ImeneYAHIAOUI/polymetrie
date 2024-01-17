from flask import Flask, request, jsonify
import psycopg2
import redis
from dotenv import load_dotenv
from prometheus_client import Counter, Histogram, generate_latest, REGISTRY, Gauge
import os
import time
app = Flask(__name__)

load_dotenv()

http_calls_total = Counter('http_calls_total', 'Total number of HTTP calls made on the webservice', ['endpoint'])
request_processing_time = Histogram('requests_processing_time', 'Processing time of requests')
memory_usage = Gauge('memory_usage', 'Memory usage of the webservice')
cpu_usage = Gauge('cpu_usage', 'CPU usage of the webservice')
# Connexion à la base de données PostgreSQL
conn_postgres = psycopg2.connect(
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT')
)
conn_postgres.set_client_encoding('UNICODE')
cursor_postgres = conn_postgres.cursor()

cursor_postgres.execute("CREATE TABLE IF NOT EXISTS clients (client_id SERIAL PRIMARY KEY, client_url VARCHAR(255) NOT NULL)")

# Connexion à Redis
conn_redis = redis.StrictRedis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'),password=os.getenv('REDIS_PASSWORD'), decode_responses=True)

@app.route('/api/visits', methods=['POST'])
@request_processing_time.time()
def track_visit():
    http_calls_total.labels(endpoint='/api/visits').inc()
    start_time = time.time() 

    data = request.json  # Récupérer les données JSON envoyées

    # Vérifier si le client est enregistré dans la base de données PostgreSQL
    client_url = data['tracker']['WINDOW_LOCATION_HREF']
    cursor_postgres.execute("SELECT * FROM clients;")
    client = cursor_postgres.fetchall()
    print(client)
    
    res = False
    for row in client:
        
        print(f"row [1] : {row[1]}")
        print(f"client url {client_url}")
        
        if row[1] in  client_url  :
            res = True

    if res:
        # Si le client est enregistré, incrémenter le compteur de visite dans Redis
        

        page_url = client_url 
        conn_redis.incr(page_url)  # Incrémentation du compteur pour cette page
        processing_time = time.time() - start_time
        request_processing_time.observe(processing_time)
        return jsonify({'message': 'Visite enregistrée avec succès'})
    else:
        processing_time = time.time() - start_time
        request_processing_time.observe(processing_time)
        return jsonify({'message': 'Client non autorisé'}), 403  # Accès interdit
    
    


## do a route to fill the database with the clients
@app.route('/api/clients', methods=['POST'])
def add_client():
    http_calls_total.labels(endpoint='/api/clients').inc()
    client_urls = [
        "https://polytech.univ-cotedazur.fr",
        "www.google.com",
        "https://www.youtube.com"
    ]

    for url in client_urls:
        # Check if the client URL already exists in the database
        cursor_postgres.execute("SELECT * FROM clients WHERE client_url = %s", (url,))
        existing_client = cursor_postgres.fetchone()

        if existing_client:
            continue  # URL already exists, skip adding

        # Insert the client URL into the PostgreSQL database
        cursor_postgres.execute("INSERT INTO clients (client_url) VALUES (%s)", (url,))
        conn_postgres.commit()  # Commit the changes to the database
        

    return jsonify({'message': 'Clients added successfully'})

@app.route('/api/fetch-db', methods=['GET'])
def fetch_db():
    http_calls_total.labels(endpoint='/api/fetch-db').inc()
    cursor_postgres.execute("SELECT * FROM clients")
    clients = cursor_postgres.fetchall()

    return jsonify({'clients': clients})


@app.route('/api/fetch-redis', methods=['GET'])
def fetch_redis():
    http_calls_total.labels(endpoint='/api/fetch-redis').inc()
    ## print keys and values
    keys = conn_redis.keys()
    values = conn_redis.mget(keys)
    ## return a list of tuples (key, value)
    return jsonify({'visits': list(zip(keys, values))})

@app.route('/metrics', methods=['GET'])
def metrics():
    # Collect and return Prometheus metrics
    return generate_latest(REGISTRY)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
