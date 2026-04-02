import os
from fastapi import APIRouter, HTTPException
import psycopg2

router = APIRouter()

@router.post("/migrate-db", tags=["Migration"], summary="Run DB Migrations", description="Apply all SQL migrations.")
def migrate_db():
    sql_dir = os.path.join(os.path.dirname(__file__), "..", "migrations")
    sql_files = [f for f in os.listdir(sql_dir) if f.endswith(".sql")]
    if not sql_files:
        raise HTTPException(status_code=404, detail="No SQL files found")
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "tradeship"),
        user=os.getenv("POSTGRES_USER", "user"),
        password=os.getenv("POSTGRES_PASSWORD", "password"),
        host=os.getenv("POSTGRES_HOST", "postgres-database"),
        port=os.getenv("POSTGRES_PORT", "5432")
    )
    cur = conn.cursor()
    # Only create schema_migrations table, do not use for versioning
    cur.execute("""
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version VARCHAR(100) PRIMARY KEY,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    applied = []
    cur.execute("SELECT version FROM schema_migrations;")
    applied_versions = {row[0] for row in cur.fetchall()}
    for sql_file in sorted(sql_files):
        if sql_file in applied_versions:
            continue
        with open(os.path.join(sql_dir, sql_file), "r") as f:
            cur.execute(f.read())
        cur.execute("INSERT INTO schema_migrations (version) VALUES (%s)", (sql_file,))
        applied.append(sql_file)
    conn.commit()
    cur.close()
    conn.close()
    return {"status": "migrations applied", "files": applied}
