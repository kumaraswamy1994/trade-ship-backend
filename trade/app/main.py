

from fastapi import FastAPI, Depends

from shared_utils.auth import get_current_user, RoleChecker
from .auth import router as auth_router




app = FastAPI(title="Trade Service API", description="APIs for trade operations.", version="1.0.0")
app.include_router(auth_router, tags=["Auth"])


@app.get("/health", tags=["Health"], summary="Health Check", description="Check if the Trade service is running.")
def health():
    return {"status": "ok"}


@app.get("/trade-data", tags=["Trade"], summary="Get Trade Data", description="Get trade data, requires 'trade' or 'admin' role.")
def trade_data(user=Depends(get_current_user), role=Depends(RoleChecker(["trade", "admin"]))):
    return {"data": "trade info"}
