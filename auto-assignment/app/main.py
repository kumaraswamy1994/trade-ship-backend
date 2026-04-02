

from fastapi import FastAPI, Depends
from shared_utils.auth import get_current_user, RoleChecker



app = FastAPI(title="Auto-Assignment Service API", description="APIs for auto-assignment operations.", version="1.0.0")


@app.get("/health", tags=["Health"], summary="Health Check", description="Check if the Auto-Assignment service is running.")
def health():
    return {"status": "ok"}


@app.get("/auto-assign-data", tags=["Auto-Assignment"], summary="Get Auto-Assignment Data", description="Get auto-assignment data, requires 'admin' role.")
def auto_assign_data(user=Depends(get_current_user), role=Depends(RoleChecker(["admin"]))):
    return {"data": "auto assignment info"}
