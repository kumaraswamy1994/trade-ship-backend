
from fastapi import APIRouter, HTTPException, status, Depends
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


class RefreshRequest(BaseModel):
    refresh_token: str


class UserSignup(BaseModel):
    username: str
    password: str
    role: str = "admin"
    email: str
    phone: str


class UserLogin(BaseModel):
    email_or_phone: str  # email or phone
    password: str


@router.post("/signup", tags=["Auth"], summary="User Sign Up", description="Sign up a new user (admin, trade, transport, etc.).")
def signup(user: UserSignup):
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
            "INSERT INTO admin.users (username, password, role, email, phone) VALUES (%s, %s, %s, %s, %s)",
            (user.username, hashed_password, user.role, user.email, user.phone)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        raise HTTPException(status_code=400, detail="User already exists or error: " + str(e))
    cur.close()
    conn.close()
    return {"message": f"{user.role.capitalize()} user created"}


@router.post("/login", tags=["Auth"], summary="User Login", description="Login for any user and get JWT and refresh token.")

def login(user: UserLogin):
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "tradeship"),
        user=os.getenv("POSTGRES_USER", "user"),
        password=os.getenv("POSTGRES_PASSWORD", "password"),
        host=os.getenv("POSTGRES_HOST", "postgres-database"),
        port=os.getenv("POSTGRES_PORT", "5432")
    )
    cur = conn.cursor()
    # Try login by email first, then by phone
    cur.execute("SELECT password, role, email, phone, username FROM admin.users WHERE email=%s OR phone=%s", (user.email_or_phone, user.email_or_phone))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row or not pwd_context.verify(user.password, row[0]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    # Access token (short-lived)
    access_payload = {
        "role": row[1],
        "email": row[2],
        "phone": row[3],
        "exp": datetime.utcnow() + timedelta(minutes=15),
        "iat": datetime.utcnow(),
        "sub": row[4]
    }
    access_token = jwt.encode(access_payload, SECRET_KEY, algorithm=ALGORITHM)
    # Refresh token (longer-lived)
    refresh_payload = {
        "sub": row[4],
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
