from fastapi import APIRouter

router = APIRouter(prefix="/transportation", tags=["transportation"])

@router.get("/")
def get_transportations():
    return {"transportations": []}
