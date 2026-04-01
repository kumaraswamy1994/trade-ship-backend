from fastapi import APIRouter

router = APIRouter(prefix="/trade", tags=["trade"])

@router.get("/")
def get_trades():
    return {"trades": []}
