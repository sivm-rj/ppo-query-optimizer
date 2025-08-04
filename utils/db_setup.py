# utils/db_setup.py

import psycopg2
from config import RAILWAY_DB_URL, NUM_TABLES

def setup_postgres_tables():
    try:
        conn = psycopg2.connect(RAILWAY_DB_URL)
        cur = conn.cursor()

        # Step 1: Create tables t0 to tN
        for i in range(NUM_TABLES):
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS t{i} (
                    id INT PRIMARY KEY,
                    fk INT
                );
            """)

        # Step 2: Insert 2 sample rows into each table
        for i in range(NUM_TABLES):
            cur.execute(f"""
                INSERT INTO t{i} (id, fk)
                VALUES (1, 1), (2, 2)
                ON CONFLICT (id) DO NOTHING;
            """)

        conn.commit()
        cur.close()
        conn.close()
        print(f"PostgreSQL tables t0 to t{NUM_TABLES - 1} created and populated.")
    
    except Exception as e:
        print("Failed to set up database:", e)

# Optional: allow direct script execution
if __name__ == "__main__":
    setup_postgres_tables()
