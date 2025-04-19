import pandas as pd
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def init_db():
    DB_NAME = "churn_db"
    DB_USER = "postgres"
    DB_PASS = "Postgres2019!"
    DB_HOST = "db"
    DB_PORT = "5432"
    CSV_PATH = "data/customer_churn_sample.csv"
    TABLE_NAME = "customer_churn"

    # Connect to default DB to create target DB if needed
    conn = psycopg2.connect(dbname="postgres", user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(f"SELECT 1 FROM pg_database WHERE datname='{DB_NAME}'")
    if not cur.fetchone():
        cur.execute(f"CREATE DATABASE {DB_NAME}")
        print(f"Database '{DB_NAME}' created.")
    cur.close()
    conn.close()

    # Connect to target DB
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()

    # Check if table exists
    cur.execute(f"SELECT to_regclass('{TABLE_NAME}')")
    if cur.fetchone()[0]:
        print("Table already exists. Skipping initialization.")
        cur.close()
        conn.close()
        return

    df = pd.read_csv(CSV_PATH)

    # Create table from schema
    cur.execute(f"DROP TABLE IF EXISTS {TABLE_NAME}")
    cols = ", ".join([f'"{col}" TEXT' for col in df.columns])
    cur.execute(f'CREATE TABLE {TABLE_NAME} ({cols})')

    for row in df.itertuples(index=False):
        values = tuple(str(val) for val in row)
        placeholders = ', '.join(['%s'] * len(values))
        cur.execute(f'INSERT INTO {TABLE_NAME} VALUES ({placeholders})', values)

    conn.commit()
    cur.close()
    conn.close()
    print("Table created and data inserted.")
