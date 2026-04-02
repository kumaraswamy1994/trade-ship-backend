from fastapi import FastAPI
from shared_utils.db_migration import router as migration_router

app = FastAPI(title="Core Service API", description="Generic and migration APIs.", version="1.0.0")
app.include_router(migration_router, tags=["Migration"])

@app.get("/health", tags=["Health"], summary="Health Check", description="Check if the Core service is running.")
def health():
    return {"status": "ok"}
