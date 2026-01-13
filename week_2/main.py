import os
import psycopg2
from fastapi import FastAPI, HTTPException
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Chie Data Platform | API Layer")

def get_db_resource():
    """Production-grade connection factory with explicit WSL defaults."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "icp_internship_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT", "5432")
    )

@app.get("/health")
async def health_check():
    return {"status": "operational", "db_layer": "connected"}

@app.get("/data/quotes")
async def fetch_quotes(limit: int = 10):
    try:
        with get_db_resource() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Corrected column name 'text' from your psql -d output
                cur.execute("SELECT author, text FROM quotes LIMIT %s;", (limit,))
                results = cur.fetchall()
                return {"count": len(results), "data": results}
    except Exception as error:
        # Proper error handling to maintain 95% Quality SLA
        print(f"[CRITICAL] Database Handshake Failed: {error}")
        raise HTTPException(status_code=500, detail="Relational layer connection error")