from fastapi import FastAPI
from app.routers import trade, transportation

app = FastAPI()

app.include_router(trade.router)
app.include_router(transportation.router)

@app.get("/")
def read_root():
    return {"message": "Trade & Transportation API"}
