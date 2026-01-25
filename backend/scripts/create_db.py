import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
import sys

# Add backend to path to import config
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from app.core.config import settings

def create_database():
    # Connect to default 'postgres' db to create the new db
    default_db = "postgres"
    
    try:
        con = psycopg2.connect(
            dbname=default_db,
            user=settings.POSTGRES_USER,
            host=settings.POSTGRES_SERVER,
            password=settings.POSTGRES_PASSWORD,
            port=settings.POSTGRES_PORT
        )
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        
        # Check if db exists
        cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{settings.POSTGRES_DB}'")
        exists = cur.fetchone()
        
        if not exists:
            print(f"Database {settings.POSTGRES_DB} does not exist. Creating...")
            cur.execute(f"CREATE DATABASE {settings.POSTGRES_DB}")
            print(f"Database {settings.POSTGRES_DB} created successfully.")
        else:
            print(f"Database {settings.POSTGRES_DB} already exists.")
            
        cur.close()
        con.close()
        return True
        
    except Exception as e:
        print(f"Error creating database: {e}")
        return False

if __name__ == "__main__":
    create_database()
