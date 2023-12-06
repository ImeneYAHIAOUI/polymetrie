from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# PostgreSQL connection details
postgres_url = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/polymetrie");

# Redis connection details
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = os.getenv("REDIS_PORT", 6379)
redis_password = os.getenv("REDIS_PASSWORD", "")

redis_url = f"redis://:{redis_password}@{redis_host}:{redis_port}/1"

