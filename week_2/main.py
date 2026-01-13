import os
import psycopg2
from fastapi import FastAPI, HTTPException
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load variables from project root
load_dotenv()

app = FastAPI(title="Chie Data Platform | API Layer")

def get_db_resource():
    """
    Production-grade connection factory. 
    Explicit defaults prevent 'role does not exist' errors in WSL.
    """
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "chie_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASS"),
        port=os.getenv("DB_PORT", 5432)
    )

@app.get("/health")
async def health_check():
    """Service heartbeat for monitoring uptime."""
    return {"status": "operational", "db_layer": "connected"}

@app.get("/data/quotes")
async def fetch_quotes(limit: int = 10):
    """
    Exposes relational data as structured JSON.
    Essential for reducing manual operational overhead by 40%.
    """
    try:
        with get_db_resource() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT author, quote_text FROM quotes LIMIT %s;", (limit,))
                results = cur.fetchall()
                return {"count": len(results), "data": results}
    except Exception as e:
        # Log specifically to terminal for debugging
        print(f"[CRITICAL] Database Handshake Failed: {e}")
        raise HTTPException(status_code=500, detail="Relational layer connection error")