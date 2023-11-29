from service import app
from models.postgres_models import Client

postgres_session = app.config["POSTGRES_SESSION"]

def add_client(name, url, email, phone):
    new_client = Client(name=name, url=url, email=email, phone=phone)
    postgres_session.add(new_client)
    postgres_session.commit() 
    return {"id": new_client.id, "name": new_client.name, "url": new_client.url, "email": new_client.email, "phone": new_client.phone}

def query_all_clients():
    clients = postgres_session.query(Client).all()
    if clients:
        result = []
        for client in clients:
            result.append({"id": client.id, "name": client.name})
        return {"count": len(result), "clients": result}
    else:
        return {"count": 0, "clients": []}

def query_client_by_id(client_id):
    client = postgres_session.query(Client).filter(Client.id == client_id).first()
    if client:
        return client
    else:
        raise Exception("Client not found.")
    

def query_client_by_url(url):
    client = postgres_session.query(Client).filter(Client.url == url).first()
    if client:
        return {"id": client.id, "name": client.name, "url": client.url}
    else:
        raise Exception("Client not found.")