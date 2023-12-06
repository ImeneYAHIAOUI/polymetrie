from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Db url
from config.db import postgres_url

Base = declarative_base()

# Clients table
class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    url = Column(String(50))
    email = Column(String(50))
    phone = Column(String(50))


# Tables creation
def create_postgres_engine_and_session(postgres_url):
    engine = create_engine(postgres_url)
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    print("Table 'clients' created successfully.")
    return Session()
