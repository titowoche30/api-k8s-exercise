import os

POSTGRES_HOST = (os.getenv('POSTGRES_HOST') or '127.0.0.1')
POSTGRES_USER = (os.getenv('POSTGRES_USER') or 'postgres')
POSTGRES_PASSWORD = (os.getenv('POSTGRES_PASSWORD') or 'postgres')
POSTGRES_DB = (os.getenv('POSTGRES_DB') or 'fastapi')
POSTGRES_PORT = (os.getenv('POSTGRES_PORT') or 5432)
