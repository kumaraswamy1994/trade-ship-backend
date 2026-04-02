from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
import psycopg2
import os
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

class TradeUserSignup(BaseModel):
    username: str
    password: str
    email: str
    phone_number: str
    full_name: str = None
    aadhar_number: str
    gst_number: str
    gst_verified: bool = False
    email_verified: bool = False
    aadhar_verified: bool = False

class TradeUserLogin(BaseModel):
    email_or_phone: str
    password: str

@router.post("/signup", tags=["Auth"], summary="Trade User Sign Up")
def signup(user: TradeUserSignup):
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "tradeship"),
        user=os.getenv("POSTGRES_USER", "user"),
        password=os.getenv("POSTGRES_PASSWORD", "password"),
        host=os.getenv("POSTGRES_HOST", "postgres-database"),
        port=os.getenv("POSTGRES_PORT", "5432")
    )
    cur = conn.cursor()
    hashed_password = pwd_context.hash(user.password)
    try:
        cur.execute(
            "INSERT INTO trade.trade_users (username, email, phone_number, full_name, hashed_password, aadhar_number, gst_number, gst_verified, email_verified, aadhar_verified) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (user.username, user.email, user.phone_number, user.full_name, hashed_password, user.aadhar_number, user.gst_number, user.gst_verified, user.email_verified, user.aadhar_verified)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        raise HTTPException(status_code=400, detail="User already exists or error: " + str(e))
    cur.close()
    conn.close()
    return {"message": "Trade user created"}

@router.post("/login", tags=["Auth"], summary="Trade User Login")
def login(user: TradeUserLogin):
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "tradeship"),
        user=os.getenv("POSTGRES_USER", "user"),
        password=os.getenv("POSTGRES_PASSWORD", "password"),
        host=os.getenv("POSTGRES_HOST", "postgres-database"),
        port=os.getenv("POSTGRES_PORT", "5432")
    )
    cur = conn.cursor()
    cur.execute("SELECT hashed_password, username, email, phone_number, role FROM trade.trade_users WHERE email=%s OR phone_number=%s", (user.email_or_phone, user.email_or_phone))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row or not pwd_context.verify(user.password, row[0]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_payload = {
        "username": row[1],
        "email": row[2],
        "phone_number": row[3],
        "role": row[4],
        "exp": datetime.utcnow() + timedelta(minutes=15),
        "iat": datetime.utcnow(),
        "sub": row[1]
    }
    access_token = jwt.encode(access_payload, SECRET_KEY, algorithm=ALGORITHM)
    refresh_payload = {
        "sub": row[1],
        "type": "refresh",
        "exp": datetime.utcnow() + timedelta(days=7),
        "iat": datetime.utcnow()
    }
    refresh_token = jwt.encode(refresh_payload, SECRET_KEY, algorithm=ALGORITHM)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
