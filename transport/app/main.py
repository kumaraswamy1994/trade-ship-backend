

from fastapi import FastAPI, Depends

from shared_utils.auth import get_current_user, RoleChecker
from .auth import router as auth_router




app = FastAPI(title="Transport Service API", description="APIs for transport operations.", version="1.0.0")
app.include_router(auth_router, tags=["Auth"])


@app.get("/health", tags=["Health"], summary="Health Check", description="Check if the Transport service is running.")
def health():
    return {"status": "ok"}


@app.get("/transport-data", tags=["Transport"], summary="Get Transport Data", description="Get transport data, requires 'transport' or 'admin' role.")
def transport_data(user=Depends(get_current_user), role=Depends(RoleChecker(["transport", "admin"]))):
    return {"data": "transport info"}
